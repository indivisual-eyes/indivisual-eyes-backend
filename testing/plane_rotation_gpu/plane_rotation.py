import numpy as np
from skimage import io, color
import matplotlib.pyplot as plt
import torch
from torch.backends import mps

device = 'cuda' if torch.cuda.is_available() else 'mps' if mps.is_available() else 'cpu'


def tensor(array):
    return torch.tensor(array, dtype=torch.float32, device=device)


def get_max_loss_normal(original_image, dichromat_image):
    height, width = original_image.shape[:2]
    variance = 2 / np.pi * np.sqrt(2 * min(width, height))

    chromaticity_vectors = []

    for row in range(height):
        for col in range(width):
            original_pixel = original_image[row][col][1:]
            dichromat_pixel = dichromat_image[row][col][1:]

            neighbor_row, neighbor_col = -1, -1

            while 0 <= neighbor_row < height:
                neighbor_row = int(np.random.normal(loc=row, scale=variance))

            while 0 <= neighbor_col < width:
                neighbor_col = int(np.random.normal(loc=col, scale=variance))

            original_neighbor_pixel = original_image[neighbor_row][neighbor_col][1:]
            dichromat_neighbor_pixel = dichromat_image[neighbor_row][neighbor_col][1:]

            direction = original_pixel - original_neighbor_pixel

            original_pixel_difference = torch.linalg.vector_norm(direction)
            dichromat_pixel_difference = torch.linalg.vector_norm(dichromat_pixel - dichromat_neighbor_pixel)

            loss = 0

            if original_pixel_difference > 0:
                loss = 1 - dichromat_pixel_difference / original_pixel_difference

            chromaticity_vectors.append(loss * direction)

    chromaticity_vectors = tensor([chromaticity_vectors])

    matrix = chromaticity_vectors.T @ chromaticity_vectors

    eigen_values, eigen_vectors = np.linalg.eig(matrix)
    a, b = eigen_vectors[np.argmax(np.abs(eigen_values))]

    return tensor([0, -b, a])


dichromat_angles = {
    'protanopia': 11.48,
    'deuteranopia': 8.11,
    'tritanopia': -46.37,
}

dichromat_angle = tensor(np.radians(dichromat_angles['protanopia']))
image_path = 'images/boat_screenshot.png'

original_image = tensor(color.rgb2lab(io.imread(image_path)[:, :, :3]))

# Project image to dichromat plane
dichromat_normal = tensor([0, torch.cos(dichromat_angle), torch.sin(dichromat_angle)])
dichromat_image = original_image - original_image[:, :, torch.newaxis] @ dichromat_normal * dichromat_normal

# Compute maximum contrast loss angle
# max_loss_normal = get_max_loss_normal(original_image, dichromat_image)
max_loss_normal = tensor([0, 0, 1])

# Project image to maximum contrast loss plane
recolored_image = original_image - original_image[:, :, np.newaxis] @ max_loss_normal * max_loss_normal

# Rotate to align with dichromat plane
angle = torch.arccos(torch.dot(dichromat_normal, max_loss_normal)) + torch.pi
transform_matrix = tensor([[1, 0, 0], [0, torch.cos(angle), -torch.sin(angle)], [0, torch.sin(angle), torch.cos(angle)]])
recolored_image = recolored_image @ transform_matrix

# Display images
fig, axes = plt.subplots(1, 3)
plt.setp(axes, xticks=[], yticks=[])

axes[0].imshow(color.lab2rgb(original_image.cpu()))
axes[1].imshow(color.lab2rgb(dichromat_image.cpu()))
axes[2].imshow(color.lab2rgb(recolored_image.cpu()))

plt.show()

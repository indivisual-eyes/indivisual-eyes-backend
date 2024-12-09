import numpy as np
from skimage import io, color
import matplotlib.pyplot as plt

dichromat_angles = {
    'protanopia': 11.48,
    'deuteranopia': 8.11,
    'tritanopia': -46.37,
}

dichromat_angle = np.radians(dichromat_angles['protanopia'])
image_path = 'images/boat_screenshot.png'

original_image = color.rgb2lab(io.imread(image_path)[:, :, :3])

height, width = original_image.shape[:2]
variance = 2 / np.pi * np.sqrt(2 * min(width, height))

dichromat_image = np.zeros(original_image.shape)
recolored_image = np.zeros(original_image.shape)

dichromat_normal = (0, np.cos(dichromat_angle), np.sin(dichromat_angle))

chromaticity_vectors = []

for row in range(height):
    for col in range(width):
        original_pixel = original_image[row][col]

        dichromat_pixel = original_pixel - np.dot(original_pixel[np.newaxis], dichromat_normal) * dichromat_normal
        dichromat_image[row][col] = dichromat_pixel

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

        original_pixel_difference = np.linalg.norm(direction)
        dichromat_pixel_difference = np.linalg.norm(dichromat_pixel - dichromat_neighbor_pixel)

        loss = 0

        if original_pixel_difference > 0:
            loss = 1 - dichromat_pixel_difference / original_pixel_difference

        chromaticity_vectors.append(loss * direction)

chromaticity_vectors = np.array(chromaticity_vectors)

matrix = chromaticity_vectors.T @ chromaticity_vectors

eigen_values, eigen_vectors = np.linalg.eig(matrix)
a, b = eigen_vectors[np.argmax(np.abs(eigen_values))]

max_loss_normal = (0, -b, a)

angle = np.arccos(np.dot(dichromat_normal, max_loss_normal)) + np.pi
transform_matrix = ((1, 0, 0), (0, np.cos(angle), -np.sin(angle)), (0, np.sin(angle), np.cos(angle)))

for row in range(height):
    for col in range(width):
        original_pixel = original_image[row][col]

        recolored_pixel = original_pixel - np.dot(original_pixel[np.newaxis], max_loss_normal) * max_loss_normal
        recolored_pixel = np.dot(recolored_pixel, transform_matrix)

        recolored_image[row][col] = recolored_pixel

fig, axes = plt.subplots(1, 3)
plt.setp(axes, xticks=[], yticks=[])

axes[0].imshow(color.lab2rgb(original_image))
axes[1].imshow(color.lab2rgb(dichromat_image))
axes[2].imshow(color.lab2rgb(recolored_image))

plt.show()

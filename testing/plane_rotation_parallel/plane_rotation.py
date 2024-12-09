import numpy as np
from skimage import io, color
from max_loss_normal import get_max_loss_normal
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

dichromat_image = np.zeros(original_image.shape)
recolored_image = np.zeros(original_image.shape)

dichromat_normal = (0, np.cos(dichromat_angle), np.sin(dichromat_angle))

for row in range(height):
    for col in range(width):
        original_pixel = original_image[row][col]

        dichromat_pixel = original_pixel - np.dot(original_pixel[np.newaxis], dichromat_normal) * dichromat_normal
        dichromat_image[row][col] = dichromat_pixel

max_loss_normal = get_max_loss_normal(original_image, dichromat_image)

for row in range(height):
    for col in range(width):
        original_pixel = original_image[row][col]

        recolored_pixel = original_pixel - np.dot(original_pixel[np.newaxis], max_loss_normal) * max_loss_normal

        angle = np.arccos(np.dot(dichromat_normal, max_loss_normal)) + np.pi
        transform_matrix = ((1, 0, 0), (0, np.cos(angle), -np.sin(angle)), (0, np.sin(angle), np.cos(angle)))
        recolored_pixel = np.dot(recolored_pixel, transform_matrix)

        recolored_image[row][col] = recolored_pixel

fig, axes = plt.subplots(1, 3)
plt.setp(axes, xticks=[], yticks=[])

axes[0].imshow(color.lab2rgb(original_image))
axes[1].imshow(color.lab2rgb(dichromat_image))
axes[2].imshow(color.lab2rgb(recolored_image))

plt.show()

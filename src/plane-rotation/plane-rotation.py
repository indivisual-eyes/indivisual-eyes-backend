import numpy as np
from skimage import io, color
import loss_evaluation
import matplotlib.pyplot as plt

dichromat_angles = {
    'protanopia': 11.48,
    'deuteranopia': 8.11,
    'tritanopia': -46.37,
}

dichromat_angle = np.radians(dichromat_angles['protanopia'])
image_path = 'images/boat_screenshot.png'

original_image = color.rgb2lab(io.imread(image_path)[:, :, :3])

# Project image to dichromat plane
dichromat_normal = (0, np.cos(dichromat_angle), np.sin(dichromat_angle))
dichromat_image = original_image - np.dot(original_image[:, :, np.newaxis], dichromat_normal) * dichromat_normal

# Compute maximum contrast loss angle
max_loss_normal = loss_evaluation.evaluate(original_image, dichromat_image)
max_loss_normal = (0, max_loss_normal[1], max_loss_normal[0])

# Project image to maximum contrast loss plane
recolored_image = original_image - np.dot(original_image[:, :, np.newaxis], max_loss_normal) * max_loss_normal

# Rotate to align with dichromat plane
angle = np.arccos(np.dot(dichromat_normal, max_loss_normal)) + np.pi
transform_matrix = ((1, 0, 0), (0, np.cos(angle), -np.sin(angle)), (0, np.sin(angle), np.cos(angle)))
recolored_image = np.dot(recolored_image, transform_matrix)

# Display images
fig, axes = plt.subplots(1, 3)
plt.setp(axes, xticks=[], yticks=[])

axes[0].imshow(color.lab2rgb(original_image))
axes[1].imshow(color.lab2rgb(dichromat_image))
axes[2].imshow(color.lab2rgb(recolored_image))

plt.show()

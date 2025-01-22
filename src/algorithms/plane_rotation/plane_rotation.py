import numpy as np
from skimage import io, color
from src.algorithms.plane_rotation.max_loss_normal import get_max_loss_normal
from PIL import Image


def plane_rotation(image_path, cvd_type):
    dichromat_angles = {
        'protanopia': 11.48,
        'deuteranopia': 8.11,
        'tritanopia': -46.37,
    }

    dichromat_angle = np.radians(dichromat_angles[cvd_type])
    original_image = color.rgb2lab(io.imread(image_path)[:, :, :3])

    dichromat_normal = (0, np.cos(dichromat_angle), np.sin(dichromat_angle))
    dichromat_image = original_image - original_image[:, :, np.newaxis] @ dichromat_normal * dichromat_normal

    max_loss_normal = get_max_loss_normal(original_image, dichromat_image)

    recolored_image = original_image - original_image[:, :, np.newaxis] @ max_loss_normal * max_loss_normal

    angle = np.arccos(np.dot(dichromat_normal, max_loss_normal)) + np.pi
    transform_matrix = ((1, 0, 0), (0, np.cos(angle), -np.sin(angle)), (0, np.sin(angle), np.cos(angle)))
    recolored_image = recolored_image @ transform_matrix

    return Image.fromarray((color.lab2rgb(recolored_image) * 255).astype(np.uint8))


import numpy as np
from skimage import io, color
from PIL import Image

dichromat_angles = {
        'protanopia': 11.48,
        'deuteranopia': 8.11,
        'tritanopia': -46.37,
    }
dichromat_angle = np.radians(dichromat_angles['protanopia'])
dichromat_normal = (0, np.cos(dichromat_angle), np.sin(dichromat_angle))
print(dichromat_normal)



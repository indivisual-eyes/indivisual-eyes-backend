import cv2
import numpy as np
import aaa_scaling_CDV as scale
import sys
from skspatial.objects import Plane, Vector
import matplotlib.pyplot as plt

# np.set_printoptions(threshold='truncated')

# Load the image in BGR format
filepath = 'wip/outside.jpg'
new_file_path = scale.simulate_cvd(filepath, 'protanopia', 50)
src = cv2.imread(new_file_path)

# Convert from BGR to CIE Lab color space (CIELAB)
converted = cv2.cvtColor(src, cv2.COLOR_BGR2LAB)

# Split the channels into L, a, b
L, a, b = cv2.split(converted)

# Ensure the a and b channels are in the proper range [-128, 127]
L = np.floor(L * 0.390625).astype(np.uint8)
a = a - 128
b = b - 128

# Stack the channels back together into a single image with correct format
lab_image = cv2.merge([L, a, b])
# print(lab_image)

#Our image is now in l*a*b format

#TODO: Define a plane that touches the X and Z axes then is rotated -11.48 degress about the z axis.

# This plane is flush with the X and Z axes.
plane = Plane((1,0,1), (0,1,0))

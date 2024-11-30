import cv2
import numpy as np
import sys
from skspatial.objects import Plane, Vector
from scipy.spatial.transform import Rotation as R
import matplotlib.pyplot as plt

# np.set_printoptions(threshold='truncated')

# Load the image in BGR format
filepath = 'wip/machado.png'

'''We might come back to this, machado has a way to project color at a percentage
we are not going to do that as of now'''
# new_file_path = scale.simulate_cvd(filepath, 'protanopia', 0)
# src = cv2.imread(new_file_path)


src = cv2.imread(filepath)

# Convert from BGR to CIE Lab color space (CIELAB)
converted = cv2.cvtColor(src, cv2.COLOR_BGR2LAB)


# Split the channels into L, a, b
L, a, b = cv2.split(converted)

#Ensure the a and b channels are in the proper range [-128, 127]
L = (L /255 * 100).clip(0,255).astype(np.float32)
a = a.astype(np.float32) - 128.0  # Shift to [-128, 127]
b = b.astype(np.float32) - 128.0 # Shift to [-128, 127]

# Stack the channels back together into a single image with correct format
lab_image = cv2.merge([L, a, b])

#Our image is now in l*a*b format

# Creating plane to represent dicromat

plane = Plane((1,0,1), (0,1,0))
rotation = R.from_euler('z', -11.48, degrees=True) #-11.48

point = np.round(rotation.apply(plane.point))
normal = np.round(rotation.apply(plane.normal))

# Plane now represents the dicromat color space
rotated_plane = Plane(point, normal)

# Creating a new matrix with the same dimensions as the image

projected = np.zeros_like(lab_image) 

num_converted = 0
for row in range(lab_image.shape[0]):
    for pixel in range(lab_image.shape[1]):
        projected[row][pixel] = rotated_plane.project_vector(lab_image[row][pixel])
        num_converted += 1
        
#loss_eval():

new_image = np.zeros_like(projected)
'''reformatting it to bgr then outputting it'''
L,a,b = cv2.split(new_image)
L = (L / 100.0 * 255.0).clip(0, 255).astype(np.uint8)
a = (a + 128).clip(0, 255).astype(np.uint8)
b = (b + 128).clip(0, 255).astype(np.uint8)

restored = cv2.merge([L,a,b])

finished_image = cv2.cvtColor(restored, cv2.COLOR_Lab2BGR) ##BGR
img = finished_image
cv2.imwrite('machado2010_test.png', img)

print('done')


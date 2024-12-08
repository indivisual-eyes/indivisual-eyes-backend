import cv2
import numpy as np
import sys
from skspatial.objects import Plane, Vector
from scipy.spatial.transform import Rotation as R
import matplotlib.pyplot as plt
import loss_evaluation as lv
import copy
# np.set_printoptions(threshold='truncated')

# Load the image in BGR format
filepath = 'wip/test_photos/machado.png'

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
lab_image = cv2.merge([L,a,b])

#Our image is now in l*a*b format

# Creating plane to represent dicromat
# xyz
plane = Plane(point=(0,0,0),normal=(0,1,0))
rotation = R.from_euler('x', 11.48, degrees=True) #-11.48

point = (rotation.apply(plane.point))
normal = (rotation.apply(plane.normal))
# removed the round, that made it not apply the rotation
print('normal', normal)
# Plane now represents the dicromat color space
rotated_plane = Plane(point, normal)


# Creating a new matrix with the same dimensions as the image

projected = np.zeros_like(lab_image) 
#Projecting the lab_image onto the dicromat's plane
for row in range(lab_image.shape[0]):
    for pixel in range(lab_image.shape[1]):
        projected[row][pixel] = rotated_plane.project_vector(lab_image[row][pixel])

# Next we project the image onto the main eigenvector plane and rotate it back to the dichromats plane
dominant_eigenvector = lv.evaluate(lab_image, projected)
dominant_eigenvector = np.append(arr = dominant_eigenvector, values = 0)



eigen_plane = Plane(point = (0,0,0), normal = dominant_eigenvector) # I need to find where to put the point
print("dominant eigen_vector", dominant_eigenvector)
new_image = np.zeros_like(lab_image)
for row in range(lab_image.shape[0]):
    for pixel in range(lab_image.shape[1]):
        new_image[row][pixel] = eigen_plane.project_vector(lab_image[row][pixel])



'''reformatting it to bgr then outputting it'''
L, a, b = cv2.split(new_image)
L = (L / 100.0 * 255.0).clip(0, 255).astype(np.uint8)
a = (a + 128).clip(0, 255).astype(np.uint8)
b = (b + 128).clip(0, 255).astype(np.uint8)

restored = cv2.merge([L,a, b])

finished_image = cv2.cvtColor(restored, cv2.COLOR_Lab2BGR) ##BGR
img = finished_image
cv2.imwrite('machado2010_test.png', img)

print('done')

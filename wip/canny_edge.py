import cv2 
import numpy as np
# Grabbing the image
file = 'high_contrast_output.png'
image = cv2.imread(file)

# Applying a funtion to convert image to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply gaussian blur, explanation of function:
# 1. The image that you are using in the function
# 2. The kernel size. The middle pixel is the one affected, but must be something like 3x3, 5x5, 7x7, etc
# 3. This is the standard deviation of the Gaussian distribution used for that Kernel. Higher value results in more blurring. 
# I honestly don't really know anything about guassian distribution
blurred_image = cv2.GaussianBlur(gray_image, (3,3), 3.0)

# Apply canny edge detection explanation of function:
# 1. The image that you are using in the function
# 2. Lower values in threshold are stronger edges
edges = cv2.Canny(gray_image, threshold1=5, threshold2=15) #CHANGE BACK TO 'blurred_image'

# Creating an image with overlay

# Creates a blank array with same dimensions (height, weight, channels)
color_edges = np.zeros_like(image)
# Wherever the value is not 0 (white in this case), fill with new value
color_edges[edges != 0] = [255, 0, 255]

# Creating an image that combines the original with the colored edges
overlay = cv2.addWeighted(image, 1, color_edges, 1, 0)

# Displaying original and edge detected
cv2.imshow('Original', image)
# cv2.imshow('blurred', blurred_image)
cv2.imshow('Edges', edges)
cv2.imshow('Overlay', overlay)
cv2.imwrite('zzoutput.png', overlay)
cv2.waitKey(0)
cv2.destroyAllWindows()


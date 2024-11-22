import cv2
import numpy as np

# Load the image
image_path = 'outside.jpg'  # Replace with your image path
image = cv2.imread(image_path)

# Define color blindness transformation matrices
protanopia_matrix = np.array([[0.567, 0.433, 0],
                              [0.558, 0.442, 0],
                              [0,     0.242, 0.758]])

deuteranopia_matrix = np.array([[0.625, 0.375, 0],
                                [0.7,   0.3,   0],
                                [0,     0.3,   0.7]])

tritanopia_matrix = np.array([[0.95,  0.05,  0],
                              [0,     0.433, 0.567],
                              [0,     0.475, 0.525]])

# Function to apply color transformation matrix
def apply_color_blindness_filter(image, matrix):
    # Normalize the image to range [0, 1]
    image = image / 255.0
    # Apply the transformation matrix to each pixel
    transformed_image = np.dot(image.reshape(-1, 3), matrix.T)
    # Reshape back to original image shape and clip to [0, 1] range
    transformed_image = transformed_image.reshape(image.shape)
    transformed_image = np.clip(transformed_image, 0, 1)
    # Convert back to [0, 255] range
    transformed_image = (transformed_image * 255).astype(np.uint8)
    return transformed_image

# Apply each filter
protanopia_image = apply_color_blindness_filter(image, protanopia_matrix)
deuteranopia_image = apply_color_blindness_filter(image, deuteranopia_matrix)
tritanopia_image = apply_color_blindness_filter(image, tritanopia_matrix)

# Display the results
cv2.imshow('Original Image', image)
cv2.imshow('Protanopia Simulation', protanopia_image)
cv2.imshow('Deuteranopia Simulation', deuteranopia_image)
cv2.imshow('Tritanopia Simulation', tritanopia_image)

# Save the results if desired
# cv2.imwrite('protanopia_image.jpg', protanopia_image)
# cv2.imwrite('deuteranopia_image.jpg', deuteranopia_image)
# cv2.imwrite('tritanopia_image.jpg', tritanopia_image)

# Wait for key press to close windows
cv2.waitKey(0)
cv2.destroyAllWindows()

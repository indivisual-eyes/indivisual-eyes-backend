import cv2
import numpy as np
import matplotlib.pyplot as plt

def daltonize(image_path, colorblind_type="protanopia"):
    """
    Daltonizes an image for a specific type of colorblindness.
    
    :param image_path: Path to the image to be daltonized.
    :param colorblind_type: Type of colorblindness ('protanopia', 'deuteranopia', 'tritanopia').
    :return: Daltonized image.
    """
    # Define LMS transformation matrices for different types of colorblindness
    colorblind_matrices = {
        "protanopia": np.array([
            [0, 1.05118294, -0.05116099],
            [0, 1, 0],
            [0, 0, 1]
        ]),
        "deuteranopia": np.array([
            [1, 0, 0],
            [0.9513092, 0, 0.04866992],
            [0, 0, 1]
        ]),
        "tritanopia": np.array([
            [1, 0, 0],
            [0, 1, 0],
            [-0.86744736, 1.86727089, 0]
        ]),
    }
    
    # Load image and convert to float for calculations
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Image at path {image_path} could not be loaded.")
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) / 255.0
    
    # Convert RGB to LMS color space
    rgb_to_lms = np.array([
        [17.8824, 43.5161, 4.11935],
        [3.45565, 27.1554, 3.86714],
        [0.0299566, 0.184309, 1.46709]
    ])
    lms_to_rgb = np.linalg.inv(rgb_to_lms)
    
    lms_image = np.dot(image.reshape(-1, 3), rgb_to_lms.T).reshape(image.shape)
    
    # Apply colorblind transformation
    cb_matrix = colorblind_matrices[colorblind_type]
    cb_lms_image = np.dot(lms_image.reshape(-1, 3), cb_matrix.T).reshape(image.shape)
    
    # Compute error and adjust colors
    error = lms_image - cb_lms_image
    adjusted_lms_image = cb_lms_image + error
    
    # Convert back to RGB
    daltonized_image = np.dot(adjusted_lms_image.reshape(-1, 3), lms_to_rgb.T).reshape(image.shape)
    daltonized_image = np.clip(daltonized_image, 0, 1)  # Clip to valid range
    
    return (daltonized_image * 255).astype(np.uint8)

# Example usage
if __name__ == "__main__":
    # Path to input image
    input_image_path = "wip/scatterplot.png"
    
    # Apply Daltonization
    try:
        daltonized_image = daltonize(input_image_path, colorblind_type="protanopia")
        
        # Display the result
        plt.figure(figsize=(10, 5))
        plt.subplot(1, 2, 1)
        plt.title("Original Image")
        original_image = cv2.cvtColor(cv2.imread(input_image_path), cv2.COLOR_BGR2RGB)
        plt.imshow(original_image)
        plt.axis("off")
        
        plt.subplot(1, 2, 2)
        plt.title("Daltonized Image")
        plt.imshow(daltonized_image)
        plt.axis("off")
        
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"Error: {e}")

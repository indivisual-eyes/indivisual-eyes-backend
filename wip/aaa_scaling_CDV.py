import numpy as np
from PIL import Image

# Define Machado's matrices for color vision deficiency (protanopia, deuteranopia, tritanopia)
CVD_MATRICES = {
    "protanopia": np.array([
        [0.567, 0.433, 0.000],
        [0.558, 0.442, 0.000],
        [0.000, 0.242, 0.758]
    ]),
    "deuteranopia": np.array([
        [0.625, 0.375, 0.000],
        [0.700, 0.300, 0.000],
        [0.000, 0.300, 0.700]
    ]),
    "tritanopia": np.array([
        [0.950, 0.050, 0.000],
        [0.000, 0.433, 0.567],
        [0.000, 0.475, 0.525]
    ])
}

def simulate_cvd(image_path, cvd_type, severity):
    """
    Simulates color vision deficiency on an image.
    
    :param image_path: Path to the image to be transformed
    :param cvd_type: Type of CVD to simulate ("protanopia", "deuteranopia", "tritanopia")
    :param severity: Severity of the CVD (0 to 100, as percentage)
    :return: Transformed image
    """
    if cvd_type not in CVD_MATRICES:
        raise ValueError(f"Invalid CVD type. Choose from {list(CVD_MATRICES.keys())}.")
    
    if not (0 <= severity <= 100):
        raise ValueError("Severity must be between 0 and 100.")
    
    # Load the image
    img = Image.open(image_path).convert("RGB")
    img_array = np.array(img, dtype=np.float32) / 255.0  # Normalize to 0-1
    
    # Select the transformation matrix
    transformation_matrix = CVD_MATRICES[cvd_type]

    # Blend between original and CVD-simulated image based on severity
    severity_factor = severity / 100.0
    transformed_array = np.dot(img_array, transformation_matrix.T)
    result_array = (1 - severity_factor) * img_array + severity_factor * transformed_array

    # Clip values to 0-1 and convert back to 8-bit format
    result_array = np.clip(result_array, 0, 1) * 255.0
    result_image = Image.fromarray(result_array.astype(np.uint8))
    r_string = '553_test.jpg'
    # result_image.save(f"cvd_{cvd_type}_{severity}.jpg")
    result_image.save(f"{r_string}")
    return r_string

# Example usage
# if __name__ == "__main__":
#     image_path = "backend/outside.jpg"  # Replace with your image path
#     cvd_type = "tritanopia"  # Choose from "protanopia", "deuteranopia", "tritanopia"
#     severity = 100  # Percentage (0-100)

#     try:
#         simulated_image = simulate_cvd(image_path, cvd_type, severity)
#         simulated_image.show()  # Show the result
#         simulated_image.save(f"cvd_{cvd_type}_{severity}.jpg")  # Save the result
#     except Exception as e:
#         print(f"Error: {e}")

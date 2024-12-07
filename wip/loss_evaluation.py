# import cv2
# import numpy as np


# def select_pixel_gaussian(height, width, center, sigma):
#     # we need the height and width of the image so that we don't select a pixel that doesn't exist
#     while True: 
#         y_offset = np.random.normal(loc= center[0], scale= sigma)
#         x_offset = np.random.normal(loc=center[1], scale=sigma)
        
#         y = int(round(y_offset))
#         x = int(round(x_offset))
        
#         if 0 <= y < height and 0 <= x < width: 
#             return  y, x
            

# def evaluate(image: cv2.typing.MatLike, p_image: cv2.typing.MatLike) -> cv2.typing.MatLike:
#     height, width = image.shape[0], image.shape[1]
#     # We are finding the maximum distance that two pixels can be apart from one another
#     max_distance = (2/np.pi)(np.sqrt(2* min(height, width))) 
    
#     difference_matrix = np.ndarray
    
#     for row in range(len(image)):
#         for pixel in range(len(row)):
#             g_pix= select_pixel_gaussian(image.shape[0], image.shape[1], [row, pixel], max_distance)
#             #calculate  (Ci -Cj) - (C'i - C'j) all over
#             #           (Ci-Cj)
#             g_y = g_pix[0]
#             g_x = g_pix[1]
            
#             ci = image[row,pixel]
#             ciprime = p_image[row, pixel]
#             cj = image[g_y, g_x]
#             cjprime= p_image[g_y,g_x]
            
#             difference = (np.linalg.norm(ci-cj) -np.linalg(ciprime- cjprime))/np.linalg.norm(ci-cj)
#             #next I want to add this difference to the matrix
#             difference_matrix[row, pixel] = difference
            
import cv2
import numpy as np


def select_pixel_gaussian(height, width, center, sigma):
    # Ensure the selected pixel is within bounds
    while True: 
        y_offset = np.random.normal(loc=center[0], scale=sigma)
        x_offset = np.random.normal(loc=center[1], scale=sigma)
        
        y = int(round(y_offset))
        x = int(round(x_offset))
        
        if 0 <= y < height and 0 <= x < width: 
            return y, x


def evaluate(image: cv2.typing.MatLike, p_image: cv2.typing.MatLike) -> cv2.typing.MatLike:
    
    height, width = image.shape[:2]
    max_distance = (2 / np.pi) * (np.sqrt(2 * min(height, width)))  # Define sigma
 
    # Initialize the difference matrix
    difference_matrix = np.zeros((height, width))

    # Initialize the M matrix to store chromaticity vectors
    chromaticity_vectors = []

    for row in range(height):
        for col in range(width):
            # Select a pixel using the Gaussian distribution
            g_y, g_x = select_pixel_gaussian(height, width, [row, col], max_distance)

            # Get pixel values
            ci = image[row, col]
            ciprime = p_image[row, col]
            cj = image[g_y, g_x]
            cjprime = p_image[g_y, g_x]

            # Compute the contrast loss
            norm_ci_cj = np.linalg.norm(ci - cj)
            norm_ciprime_cjprime = np.linalg.norm(ciprime - cjprime)

            # Avoid division by zero
            if norm_ci_cj != 0:
                loss = (norm_ci_cj - norm_ciprime_cjprime) / norm_ci_cj
            else:
                loss = 0

            # Compute the direction of contrast loss
            direction = ci - cj  # Vector in the original color space

            # Project direction onto the chromaticity plane (ignore L* component)
            chromaticity_vector = loss * direction[1:]  # [a*, b*] components only
            chromaticity_vectors.append(chromaticity_vector)

            # Store the difference in the matrix
            difference_matrix[row, col] = loss

    # Convert the list of chromaticity vectors to a NumPy array
    chromaticity_vectors = np.array(chromaticity_vectors)

    # Compute the covariance matrix of chromaticity vectors
    covariance_matrix = chromaticity_vectors.T @ chromaticity_vectors

    # Find the eigenvector corresponding to the largest eigenvalue
    eigenvalues, eigenvectors = np.linalg.eig(covariance_matrix)
    print(eigenvectors, "eigen")
    dominant_eigenvector = eigenvectors[:, np.argmax(np.abs(eigenvalues))]

    return dominant_eigenvector

    
    
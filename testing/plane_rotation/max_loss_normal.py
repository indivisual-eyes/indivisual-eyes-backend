import numpy as np


def get_max_loss_normal(original_image, dichromat_image):
    height, width = original_image.shape[:2]
    variance = 2 / np.pi * np.sqrt(2 * min(width, height))

    chromaticity_vectors = np.zeros((width * height, 2))

    for row in range(0, height, 16):
        for col in range(0, width, 16):
            original_pixel = original_image[row][col][1:]
            dichromat_pixel = dichromat_image[row][col][1:]

            neighbor_row, neighbor_col = -1, -1

            while not 0 <= neighbor_row < height:
                neighbor_row = int(np.random.normal(loc=row, scale=variance))

            while not 0 <= neighbor_col < width:
                neighbor_col = int(np.random.normal(loc=col, scale=variance))

            original_neighbor_pixel = original_image[neighbor_row][neighbor_col][1:]
            dichromat_neighbor_pixel = dichromat_image[neighbor_row][neighbor_col][1:]

            direction = original_pixel - original_neighbor_pixel

            original_pixel_difference = np.linalg.norm(direction)
            dichromat_pixel_difference = np.linalg.norm(dichromat_pixel - dichromat_neighbor_pixel)

            loss = 0

            if original_pixel_difference > 0:
                loss = 1 - dichromat_pixel_difference / original_pixel_difference

            chromaticity_vectors[row * width + col] = loss * direction

    matrix = chromaticity_vectors.T @ chromaticity_vectors

    eigen_values, eigen_vectors = np.linalg.eig(matrix)
    a, b = eigen_vectors[np.argmax(np.abs(eigen_values))]

    return 0, -b, a

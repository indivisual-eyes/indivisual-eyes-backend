import numpy as np

from PIL import Image

CVD_MATRICES = {
    'normal': np.array([
        [1.000, 0.000, 0.000],
        [0.000, 1.000, 0.000],
        [0.000, 0.000, 1.000]
    ]),
    'protanopia': np.array([
        [0.567, 0.433, 0.000],
        [0.558, 0.442, 0.000],
        [0.000, 0.242, 0.758]
    ]),
    'deuteranopia': np.array([
        [0.625, 0.375, 0.000],
        [0.700, 0.300, 0.000],
        [0.000, 0.300, 0.700]
    ]),
    'tritanopia': np.array([
        [0.950, 0.050, 0.000],
        [0.000, 0.433, 0.567],
        [0.000, 0.475, 0.525]
    ])
}


def simulate_cvd(image_path, cvd_type, severity, path=True):
    if cvd_type not in CVD_MATRICES:
        raise ValueError(f'Invalid CVD type. Choose from {list(CVD_MATRICES.keys())}.')

    if not (0 <= severity <= 100):
        raise ValueError('Severity must be between 0 and 100.')

    if path:
        img = Image.open(image_path).convert('RGB')
    else:
        img = image_path
    img_array = np.array(img, dtype=np.float32) / 255.0

    transformation_matrix = CVD_MATRICES[cvd_type]

    severity_factor = severity / 100.0
    transformed_array = np.dot(img_array, transformation_matrix.T)
    result_array = (1 - severity_factor) * img_array + severity_factor * transformed_array

    result_array = np.clip(result_array, 0, 1) * 255.0
    result_image = Image.fromarray(result_array.astype(np.uint8))

    return result_image


from matplotlib import pyplot as plt

path = 'rgb_spectrum.png'

image1 = simulate_cvd(path, 'protanopia', 0)
# image1 = simulate_cvd(image1, 'protanopia', 50, False)

image2 = simulate_cvd(path, 'protanopia', 75)
# image2 = simulate_cvd(image2, 'protanopia', 50, False)
# image2 = simulate_cvd(path, 'tritanopia', 100)

image3 = simulate_cvd(path, 'protanopia', 100)
# image3 = simulate_cvd(image3, 'protanopia', 50, False)
# image3 = simulate_cvd(path, 'tritanopia', 100)

fig, axes = plt.subplots(3, 1)
plt.setp(axes, xticks=[], yticks=[])

axes[0].imshow(image1)
axes[1].imshow(image2)
axes[2].imshow(image3)

plt.show()

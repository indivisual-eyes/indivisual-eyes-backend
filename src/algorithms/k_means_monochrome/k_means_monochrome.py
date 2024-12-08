import numpy as np
from PIL import Image
from sklearn.cluster import KMeans


def k_means_monochrome(image_path, n):
    image = Image.open(image_path).convert('RGB')
    image = np.array(image, dtype=np.float32) / 255.0

    pixels = image.reshape((-1, 3))
    kmeans = KMeans(n_clusters=n, random_state=13)
    kmeans.fit(pixels)

    palette = np.empty((0, 3), dtype=np.uint8)

    cur = 255
    n_factor = int(255 / n)

    while cur >= 0 + n_factor:
        palette = np.vstack([palette, (cur, cur, cur)])
        cur -= n_factor

    palette[n - 1] = (0, 0, 0)
    palette = palette.astype(np.uint8)

    labels = kmeans.labels_
    new_pixels = palette[labels]

    return Image.fromarray(new_pixels.reshape(image.shape))

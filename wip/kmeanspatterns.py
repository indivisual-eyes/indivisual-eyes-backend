import cv2
import numpy as np
from sklearn.cluster import KMeans

# Load images
image = cv2.imread('wip/spine.png')
p1 = cv2.imread('wip/checkerboard.jpg')
p2 = cv2.imread('wip/tesselated.png')
p3 = cv2.imread('wip/dots.jpg')

# Reshape the main image for clustering
pixels = image.reshape((-1, 3))

# Number of clusters
N =4
kmeans = KMeans(n_clusters=N, random_state=50)
kmeans.fit(pixels)

# Define a custom color palette for clusters
palette = np.array([
    [255, 0, 0],    # Red
    [0, 255, 0],    # Green
    [0, 0, 255],    # Blue
    [255, 255, 0],  # Yellow
    [255, 0, 255],  # Magenta
    [0, 255, 255]   # Cyan
], dtype=np.uint8)

# Map each pixel to the closest cluster's color
labels = kmeans.labels_
clustered_image = palette[labels].reshape(image.shape)

# Resize patterns to match the main image dimensions
patterns = [p1, p2, p3]
patterns_resized = [cv2.resize(p, (image.shape[1], image.shape[0])) for p in patterns]

# Create a blank output image
output_image = np.zeros_like(image)

# Define which clusters correspond to which patterns
cluster_to_pattern = {1: patterns_resized[0], 3: patterns_resized[1], 2: patterns_resized[2]}

# Map clusters to patterns
for cluster, pattern in cluster_to_pattern.items():
    mask = (labels.reshape(image.shape[:2]) == cluster)  # Boolean mask for the cluster
    output_image[mask] = pattern[mask]

# Fill remaining areas with the original image
remaining_mask = ~np.isin(labels.reshape(image.shape[:2]), list(cluster_to_pattern.keys()))
output_image[remaining_mask] = image[remaining_mask]

# Display the result
cv2.imshow('Pattern Image', output_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

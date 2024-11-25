import cv2
import numpy as np
from sklearn.cluster import KMeans
import plotly.graph_objects as go

# Load the image
image = cv2.imread('butterfly.jpg')

# Reshape the image to a 2D array of pixels (num_pixels, 3)
pixels = image.reshape((-1, 3))

# Set the number of desired colors (clusters) for maximum contrast
N = 30  # You can adjust the number of clusters (colors)

# Apply K-means clustering to the pixels
kmeans = KMeans(n_clusters=N, random_state=13)
kmeans.fit(pixels)

# Get the centroids (cluster centers) from K-means
centroids = kmeans.cluster_centers_  # Shape: (N, 3)

# New image using the original colors from the centroids
new_colors = kmeans.cluster_centers_[kmeans.predict(pixels)] ###.predict is really useful
reduced_color = new_colors.reshape(image.shape).astype(np.uint8)

# Display the original and reduced-color images
cv2.imshow('Original Image', image)
cv2.imshow('Reduced Color [N colors]', reduced_color)

# Save the reduced-color image
# cv2.imwrite('reduced_color_output.png', reduced_color)

# Visualize the centroids in 3D RGB space using Plotly ####################
fig = go.Figure()

# Add the centroid points as markers in 3D space
fig.add_trace(go.Scatter3d(
    x=centroids[:, 0],  # Red channel
    y=centroids[:, 1],  # Green channel
    z=centroids[:, 2],  # Blue channel
    mode='markers+text',
    marker=dict(
        size=10,
        color=centroids / 255,  # Normalize RGB values to [0, 1] for Plotly
        opacity=0.8
    ),
    text=[f'Centroid {i+1}' for i in range(N)],  # Label each centroid
    textposition='top center'
))

# Configure the 3D axes
fig.update_layout(
    scene=dict(
        xaxis=dict(title='Red'),
        yaxis=dict(title='Green'),
        zaxis=dict(title='Blue'),
    ),
    title='Centroids in RGB Color Space',
    width=700,
    height=700,
)

# Show the interactive 3D plot
fig.show()

# Wait for a key press and close the OpenCV windows
cv2.waitKey(0)
cv2.destroyAllWindows()

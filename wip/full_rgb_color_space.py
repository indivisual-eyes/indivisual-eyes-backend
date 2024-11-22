import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Generate a sample grid of RGB values
# We will sample the color space to reduce the number of points and make visualization manageable
step = 25  # Adjust step for finer or coarser sampling
r_values = np.arange(0, 256, step)
g_values = np.arange(0, 256, step)
b_values = np.arange(0, 256, step)

# Generate all combinations of r, g, and b values
colors = np.array([[r, g, b] for r in r_values for g in g_values for b in b_values])

# Normalize RGB values to range [0, 1] for displaying colors in matplotlib
colors_normalized = colors / 255.0

# Create 3D plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(colors[:, 0], colors[:, 1], colors[:, 2], c=colors_normalized, marker='o')

# Set axis labels and limits
ax.set_xlabel('Red')
ax.set_ylabel('Green')
ax.set_zlabel('Blue')
ax.set_xlim(0, 255)
ax.set_ylim(0, 255)
ax.set_zlim(0, 255)

# Set axis ticks to be in range [0, 255]
ax.set_xticks([0, 128, 255])
ax.set_yticks([0, 128, 255])
ax.set_zticks([0, 128, 255])

# Title for the plot
ax.set_title("3D RGB Color Space")

# Show plot
plt.show()

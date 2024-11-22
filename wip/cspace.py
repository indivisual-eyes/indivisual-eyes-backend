import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Define color blindness matrices
protanopia_matrix = np.array([[0.567, 0.433, 0],
                              [0.558, 0.442, 0],
                              [0,     0.242, 0.758]])

deuteranopia_matrix = np.array([[0.625, 0.375, 0],
                                [0.7,   0.3,   0],
                                [0,     0.3,   0.7]])

tritanopia_matrix = np.array([[0.95,  0.05,  0],
                              [0,     0.433, 0.567],
                              [0,     0.475, 0.525]])

# Function to apply color blindness matrix to RGB colors
def apply_color_blindness_filter(colors, matrix):
    # Apply matrix to each color
    transformed_colors = np.dot(colors, matrix.T)
    # Clip to ensure values stay within [0, 1] range
    transformed_colors = np.clip(transformed_colors, 0, 1)
    return transformed_colors

# Generate a sample grid of RGB values
step = 50  # Adjust step for finer or coarser sampling
r_values = np.arange(0, 256, step)
g_values = np.arange(0, 256, step)
b_values = np.arange(0, 256, step)

# Create all combinations of r, g, and b values and normalize
colors = np.array([[r, g, b] for r in r_values for g in g_values for b in b_values], dtype=np.float32) / 255.0

# Apply each color blindness filter
protanopia_colors = apply_color_blindness_filter(colors, protanopia_matrix)
deuteranopia_colors = apply_color_blindness_filter(colors, deuteranopia_matrix)
tritanopia_colors = apply_color_blindness_filter(colors, tritanopia_matrix)

# Function to plot the color space
def plot_rgb_color_space(ax, colors, title):
    ax.scatter(colors[:, 0] * 255, colors[:, 1] * 255, colors[:, 2] * 255, c=colors, marker='o')
    ax.set_xlabel('Red')
    ax.set_ylabel('Green')
    ax.set_zlabel('Blue')
    ax.set_xlim(0, 255)
    ax.set_ylim(0, 255)
    ax.set_zlim(0, 255)
    ax.set_xticks([0, 128, 255])
    ax.set_yticks([0, 128, 255])
    ax.set_zticks([0, 128, 255])
    ax.set_title(title)

# Plot each 3D color space
fig = plt.figure(figsize=(18, 6))

# Original RGB color space
ax1 = fig.add_subplot(131, projection='3d')
plot_rgb_color_space(ax1, colors, "Normal RGB Vision")

# Protanopia color space
ax2 = fig.add_subplot(132, projection='3d')
plot_rgb_color_space(ax2, protanopia_colors, "Protanopia Simulation")

# Deuteranopia color space
# ax3 = fig.add_subplot(133, projection='3d')
# plot_rgb_color_space(ax3, deuteranopia_colors, "Deuteranopia Simulation")

#Tritanopia color space
ax4 = fig.add_subplot(133, projection='3d')
plot_rgb_color_space(ax4, tritanopia_colors, "Tritanopia Simulation")

plt.tight_layout()
plt.show()

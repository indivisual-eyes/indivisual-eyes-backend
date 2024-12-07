import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import colorspacious as cs

# Generate RGB colors
rgb_colors = np.linspace(0, 1, 20)  # 20 steps per channel
rgb_grid = np.array(np.meshgrid(rgb_colors, rgb_colors, rgb_colors)).reshape(3, -1).T

# Convert RGB to CAM02-UCS
cam02_ucs_colors = cs.cspace_convert(rgb_grid, "sRGB1", "CAM02-UCS")

# Plot in 3D (J', a', b')
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection="3d")
ax.scatter(cam02_ucs_colors[:, 1],  # a'
           cam02_ucs_colors[:, 2],  # b'
           cam02_ucs_colors[:, 0],  # J'
           c=rgb_grid, s=5)

ax.set_xlabel("a' (Red-Green)")
ax.set_ylabel("b' (Blue-Yellow)")
ax.set_zlabel("J' (Lightness)")
plt.title("CAM02-UCS 3D Visualization")
plt.show()

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Define the normal vector
type = np.pi / 4  # Example angle (45 degrees)
normal = np.array([0, np.cos(type), np.sin(type)])

# Find an orthogonal vector
# Assume z = 1 for simplicity
z = 1
y = -z * np.tan(type)  # Compute y using the relationship from dot product
x = 1  # Choose any value for x since normal's x-component is 0
orthogonal_vector = np.array([x, y, z])

# Validate orthogonality
dot_product = np.dot(normal, orthogonal_vector)
print(f"Dot product (should be close to 0): {dot_product}")

# Visualization
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the normal vector
ax.quiver(0, 0, 0, normal[0], normal[1], normal[2], color='r', label='Normal Vector', length=1)

# Plot the orthogonal vector
ax.quiver(0, 0, 0, orthogonal_vector[0], orthogonal_vector[1], orthogonal_vector[2],
          color='b', label='Orthogonal Vector', length=1)

# Set axis labels
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Add legend
ax.legend()

# Display the plot
plt.show()

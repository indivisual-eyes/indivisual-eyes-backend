import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sympy import Plane, Point3D

# Step 1: Define the 3D point and the plane
p = Point3D(2, 2, 2)  # The point to be projected
plane_point = Point3D(126, 126, 100)  # A point on the plane
normal_vector = (0, 0, 1)  # Normal vector of the plane

# Create the plane
p1 = Plane(plane_point, normal_vector=normal_vector)

# Step 2: Calculate the projection of the point onto the plane
projectionPoint = p1.projection(p)

# Print the projection point
print(f"Projection Point: {projectionPoint}")

# Step 3: Visualization

# Create the figure and the 3D axis
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plane (for visualization, let's define it using a grid)
xx, yy = np.meshgrid(range(0, 300, 20), range(0, 300, 20))
zz = (plane_point[0] - normal_vector[0] * xx - normal_vector[1] * yy) / normal_vector[2]

# Plot the plane
ax.plot_surface(xx, yy, zz, alpha=0.5, rstride=100, cstride=100, color='blue', edgecolors='b')

# Plot the original point (in red)
ax.scatter(p[0], p[1], p[2], color='red', label='Original Point')

# Plot the projection point (in green)
ax.scatter(projectionPoint[0], projectionPoint[1], projectionPoint[2], color='green', label='Projection Point')

# Connect the point to the plane with a line
ax.plot([p[0], projectionPoint[0]], [p[1], projectionPoint[1]], [p[2], projectionPoint[2]], color='black', linestyle='--')

# Labels and title
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('3D Point and its Projection onto Plane')

# Add legend
ax.legend()

# Show the plot
plt.show()

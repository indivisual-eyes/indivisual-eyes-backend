from skspatial.objects import Plane, Vector
from scipy.spatial.transform import Rotation as R
import numpy as np

p1 = Plane((1,0,1), (0,1,0))
r1 = R.from_euler('z', 90, degrees=True)

# print(type(r1))

from skspatial.objects import Plane
from scipy.spatial.transform import Rotation as R

# Define the plane and rotation
p1 = Plane((1, 0, 1), (0, 800, 0))  # Plane defined by point (1, 0, 1) and normal (0, 1, 0)
r1 = R.from_euler('z', 90, degrees=True)  # 90-degree rotation around the z-axis


# Extract the plane's point and normal vector
point_on_plane = p1.point
normal_vector = p1.normal



# Apply the rotation to the point and the normal vector
rotated_point = np.round(r1.apply(point_on_plane), decimals=5)
rotated_normal = np.round(r1.apply(normal_vector), decimals=5)

# Create a new plane using the rotated point and normal
p2 = Plane(rotated_point, rotated_normal)

# Output the new plane

print(f"Original plane: {p1}")
print(f"Rotated plane: {p2}")


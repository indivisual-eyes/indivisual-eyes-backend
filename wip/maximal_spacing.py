import numpy as np
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Generate random 3D points
def generate_points(num_points):
    np.random.seed(42)  # For reproducibility
    points = np.random.rand(num_points, 3) # creates an array with dimentions of (x,y) our case being numpoints * 3
    for i in range(len(points)):
        points[i, 0] = (points [i, 0] * 254) - 127 # scaling it to L*a*b* color space
        points[i, 1] = (points [i, 1] * 254) - 127
        points[i, 2] = points [i, 2] * 100
    return points

# Compute convex hull
def compute_convex_hull(points):
    return ConvexHull(points)

# Visualize convex hull
def visualize_convex_hull(points, hull):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot the points
    ax.scatter(points[:, 0], points[:, 1], points[:, 2], color='blue', alpha=0.6, label='Points')
    
    # Plot the convex hull
    for simplex in hull.simplices:
        # Extract vertices for each simplex (triangle face)
        triangle = points[simplex]
        ax.add_collection3d(Poly3DCollection([triangle], alpha=0.3, edgecolor='k', facecolor='cyan'))
    
    # Label axes
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title("3D Convex Hull")
    plt.legend()
    plt.show()

# Example usage
if __name__ == "__main__":
    num_points = 1000
    points = generate_points(num_points)
    hull = compute_convex_hull(points)
    print(hull)
    visualize_convex_hull(points, hull)

import numpy as np
import matplotlib.pyplot as plt
from skimage.color import rgb2lab, lab2rgb
from matplotlib.colors import ListedColormap


# Step 1: Generate a grid of RGB colors
def generate_color_grid(resolution=10):
    """
    Generate a grid of RGB colors evenly spaced in the RGB cube.
    """
    r = np.linspace(0, 1, resolution)
    g = np.linspace(0, 1, resolution)
    b = np.linspace(0, 1, resolution)
    rgb = np.array(np.meshgrid(r, g, b)).T.reshape(-1, 3)
    return rgb


# Step 2: Simulate a colorblind view (simplified protanopia simulation)
def simulate_protanopia(rgb):
    """
    Simulate protanopia by adjusting the RGB channels.
    This is a simplified approach.
    """
    # Transformation matrix for protanopia simulation
    matrix = np.array([[0.56667, 0.43333, 0.0],
                       [0.55833, 0.44167, 0.0],
                       [0.0, 0.24167, 0.75833]])
    return np.dot(rgb, matrix.T)


# Step 3: Adjust Lab values to improve distinguishability
def adjust_lab_for_cvd(lab):
    """
    Adjust Lab values to enhance distinguishability for colorblind viewers.
    """
    lab_adjusted = lab.copy()
    # Increase chroma (a* and b* values)
    lab_adjusted[:, 1] *= 1.5  # Enhance red-green axis
    lab_adjusted[:, 2] *= 1.5  # Enhance blue-yellow axis
    return lab_adjusted


# Step 4: Visualize original, simulated, and adjusted colors
def visualize_colors(original, simulated, adjusted, resolution):
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    for ax, colors, title in zip(axes, [original, simulated, adjusted],
                                 ["Original Colors", "Simulated Protanopia", "Adjusted for CVD"]):
        ax.imshow(colors.reshape(resolution, resolution, 3), extent=(0, 1, 0, 1))
        ax.set_title(title)
        ax.axis("off")
    plt.tight_layout()
    plt.show()


# Main Workflow
if __name__ == "__main__":
    resolution = 20  # Grid resolution
    rgb_colors = generate_color_grid(resolution)  # Original RGB grid
    
    # Simulate protanopia
    simulated_rgb = simulate_protanopia(rgb_colors)
    
    # Convert to Lab
    lab_colors = rgb2lab(rgb_colors.reshape((resolution**2, 1, 3))).reshape((-1, 3))
    simulated_lab = rgb2lab(simulated_rgb.reshape((resolution**2, 1, 3))).reshape((-1, 3))
    
    # Adjust Lab for better distinguishability
    adjusted_lab = adjust_lab_for_cvd(simulated_lab)
    adjusted_rgb = lab2rgb(adjusted_lab.reshape((resolution**2, 1, 3))).reshape((-1, 3))
    
    # Ensure adjusted RGB is clipped to valid range
    adjusted_rgb = np.clip(adjusted_rgb, 0, 1)
    
    # Visualize original, simulated, and adjusted colors
    visualize_colors(
        rgb_colors.reshape((resolution, resolution, 3)),
        simulated_rgb.reshape((resolution, resolution, 3)),
        adjusted_rgb.reshape((resolution, resolution, 3)),
        resolution
    )

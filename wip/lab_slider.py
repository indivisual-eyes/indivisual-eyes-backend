import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from scipy.special import expit  # For smooth mapping from Lab to RGB


def lab_to_rgb(L, a, b):
    """
    Convert CIE Lab to RGB using standard transformation.
    This uses a simple approach to map Lab to RGB colors.
    """
    # Convert Lab to XYZ color space
    Y = (L + 16) / 116
    X = a / 500 + Y
    Z = Y - b / 200

    # Apply inverse gamma correction
    if Y ** 3 > 0.008856:
        Y = Y ** 3
    else:
        Y = (Y - 16 / 116) / 7.787

    if X ** 3 > 0.008856:
        X = X ** 3
    else:
        X = (X - 16 / 116) / 7.787

    if Z ** 3 > 0.008856:
        Z = Z ** 3
    else:
        Z = (Z - 16 / 116) / 7.787

    # Scale XYZ to RGB range
    ref_X =  95.047
    ref_Y = 100.000
    ref_Z = 108.883

    X = X * ref_X
    Y = Y * ref_Y
    Z = Z * ref_Z

    # Normalize to RGB color space
    r =  3.2406 * X - 1.5372 * Y - 0.4986 * Z
    g = -0.9689 * X + 1.8758 * Y + 0.0415 * Z
    b =  0.0557 * X - 0.2040 * Y + 1.0570 * Z

    # Clip RGB values to 0-1 range
    r = min(1, max(0, r))
    g = min(1, max(0, g))
    b = min(1, max(0, b))

    return r, g, b


# Create the interactive slider
def update_color(val):
    """
    Update the color based on the current slider values.
    """
    L = slider_L.val
    a = slider_a.val
    b = slider_b.val

    # Map Lab to RGB
    r, g, b_ = lab_to_rgb(L, a, b)

    # Update the color rectangle
    ax_color.set_facecolor([r, g, b_])
    fig.canvas.draw_idle()


# Create a base plot for visualization
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)  # Adjust the slider placement
ax_color = fig.add_axes([0.0, 0.5, 1.0, 0.5])  # The color display box
ax_color.set_facecolor([0.5, 0.5, 0.5])  # Set initial background
ax_color.set_xticks([])  # Remove axes ticks
ax_color.set_yticks([])

# Add sliders
ax_slider_L = plt.axes([0.2, 0.1, 0.65, 0.03])  # L* slider
ax_slider_a = plt.axes([0.2, 0.15, 0.65, 0.03])  # a* slider
ax_slider_b = plt.axes([0.2, 0.2, 0.65, 0.03])  # b* slider

slider_L = Slider(ax_slider_L, "L*", valmin=0, valmax=100, valinit=50)
slider_a = Slider(ax_slider_a, "a*", valmin=-128, valmax=127, valinit=0)
slider_b = Slider(ax_slider_b, "b*", valmin=-128, valmax=127, valinit=0)

# Attach the slider update
slider_L.on_changed(update_color)
slider_a.on_changed(update_color)
slider_b.on_changed(update_color)

# Render the initial visualization
update_color(None)
plt.show()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

# Function to generate the mixed color based on red and green intensities
def generate_color(red_intensity, green_intensity):
    """Generate a color based on red and green intensities."""
    return np.array([red_intensity, green_intensity, 0])

# Create the figure and axis for displaying the colors
fig, ax = plt.subplots(figsize=(8, 6))
plt.subplots_adjust(left=0.2, right=0.8, top=0.8, bottom=0.2)

# Reference Yellow color (R: 1, G: 1, B: 0)
reference_yellow = np.array([0.3, 0.7, 0])

# Plot the reference yellow color in a separate figure
fig_ref, ax_ref = plt.subplots(figsize=(8, 6))
ax_ref.add_patch(plt.Rectangle((0, 0), 1, 1, color=reference_yellow))
ax_ref.text(0.5, 0.5, 'Reference Yellow', ha='center', va='center', fontsize=16, color='black')
ax_ref.set_xlim([0, 1])
ax_ref.set_ylim([0, 1])
ax_ref.axis('off')

# Set axis limits to remove axis ticks for the main plot
ax.set_xlim([0, 1])
ax.set_ylim([0, 1])
ax.axis('off')

# Add sliders for adjusting red and green intensity
axcolor = 'lightgoldenrodyellow'

# Slider for red intensity
ax_red = plt.axes([0.2, 0.05, 0.65, 0.03], facecolor=axcolor)
slider_red = Slider(ax_red, 'Red Intensity', 0.0, 1.0, valinit=0.5)

# Slider for green intensity
ax_green = plt.axes([0.2, 0.01, 0.65, 0.03], facecolor=axcolor)
slider_green = Slider(ax_green, 'Green Intensity', 0.0, 1.0, valinit=0.5)

# Create a text box to show the RGB values of the generated color
text_ax = plt.axes([0.2, 0.15, 0.65, 0.05], facecolor='lightgray')
text_box = ax.text(0.5, 0.5, "", ha="center", va="center", fontsize=12, color="black")

# Update function to change the displayed color based on slider values
def update(val):
    red_intensity = slider_red.val
    green_intensity = slider_green.val
    
    # Generate new color based on the red and green intensities
    new_color = generate_color(red_intensity, green_intensity)
    
    # Update the background color to the new color
    ax.clear()  # Clear previous color
    ax.add_patch(plt.Rectangle((0, 0), 1, 1, color=new_color))
    
    # Redraw the reference yellow color and its label
    ax.text(0.5, 0.5, 'Generated Color', ha='center', va='center', fontsize=16, color='black')

    # Update the RGB values of the generated color
    gen_rgb = tuple(new_color)
    text_box.set_text(f"Generated RGB: {gen_rgb}")

    # Redraw the updated plot
    fig.canvas.draw_idle()

# Call the update function when sliders change
slider_red.on_changed(update)
slider_green.on_changed(update)

# Function to print RGB values of the generated color when the button is clicked
def on_button_click(event):
    # Get the current RGB values of the generated color
    red_intensity = slider_red.val
    green_intensity = slider_green.val
    
    generated_color = generate_color(red_intensity, green_intensity)
    
    # Print the RGB values of the generated color
    print(f"Generated RGB: {tuple(generated_color)}")

# Add button for displaying the RGB values of the generated color
button_ax = plt.axes([0.4, 0.2, 0.2, 0.075], facecolor='lightblue')
button = Button(button_ax, 'Show RGB Values')
button.on_clicked(on_button_click)

# Show both figures
plt.show()

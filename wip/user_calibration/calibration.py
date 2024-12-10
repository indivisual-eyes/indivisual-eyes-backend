import numpy as np
from skimage import color
import tkinter as tk
from enum import Enum

class cvd(Enum):
    P = -11.48
    D = -8.11
    T = 46.37


def generate(l: int, a: int, b: int, scale, type: cvd):
  
    normal = np.array([0, np.cos(type.value), np.sin(type.value)])
    new_color = np.array([l, a, b]) + scale * normal
    print('color', new_color)
    
    
    c1 = new_color #np.array([l+.0, a+.0, b+.0])
    #convert to rgb
    c1 = color.lab2rgb(c1)
    # reformat
    c1 = np.clip((c1 * 255).astype(int), min = 0, max =255)
    # convert to hex
    c1_hex_color = f'#{c1[0]:02x}{c1[1]:02x}{c1[2]:02x}'
    # Change the color of the displayed color
    color_1.config(bg= c1_hex_color)
    
    
    return 






# Create the main application window
app = tk.Tk()
app.title("Calibartion Tool")


# Create a label to display the resulting color
color_1 = tk.Label(app, text= "Color 1", bg = "white")
color_1.pack(pady = 10)
# Create a label to display the hex color code


# Initialize the color display
update_button = tk.Button(app, command = generate(50, 0, 0, scale= 20, type = cvd.P))
update_button.pack()

# Start the application
app.mainloop()

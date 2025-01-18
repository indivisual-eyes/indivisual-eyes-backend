import numpy as np
import random
from skimage import color
import tkinter as tk
from enum import Enum

class cvd(Enum):
    P = -11.48
    D = -8.11
    T = 46.37


def generate(l: int, a: int, b: int, scale, type: cvd):
  
    normal = np.array([0, np.cos(type.value), np.sin(type.value)])
    range = [scale, scale*2, 1]
    random.shuffle(range)
    print(range)
    
    
    color1 = np.array([l+ .0, a + .0, b+ .0] + range[2] * normal)
    color2 = np.array([l +.0,a +.0, b+.0]) + (range[0]) * normal
    color3 = np.array([l+.0, a +.0, b + .0]) + range[1] * normal
    print('color1', color1)
    print('color2', color2)
    print('color3', color3)
    
    
    c1 = color1 #np.array([l+.0, a+.0, b+.0])
    #convert to rgb
    c1 = color.lab2rgb(c1)
    # reformat
    c1 = np.clip((c1 * 255).astype(int), min = 0, max =255)
    # convert to hex
    c1_hex_color = f'#{c1[0]:02x}{c1[1]:02x}{c1[2]:02x}'
    # Change the color of the displayed color
    color_1.config(bg= c1_hex_color)
    
    c2 = color2 #np.array([l+.0, a+.0, b+.0])
    #convert to rgb
    c2 = color.lab2rgb(c2)
    # reformat
    c2 = np.clip((c2 * 255).astype(int), min = 0, max =255)
    # convert to hex
    c2_hex_color = f'#{c2[0]:02x}{c2[1]:02x}{c2[2]:02x}'
    # Change the color of the displayed color
    color_2.config(bg= c2_hex_color)
    
    c3 = color3 #np.array([l+.0, a+.0, b+.0])
    #convert to rgb
    c3 = color.lab2rgb(c3)
    # reformat
    c3 = np.clip((c3 * 255).astype(int), min = 0, max =255)
    # convert to hex
    c3_hex_color = f'#{c3[0]:02x}{c3[1]:02x}{c3[2]:02x}'
    # Change the color of the displayed color
    color_3.config(bg= c3_hex_color)
    return 






# Create the main application window
app = tk.Tk()
app.title("Calibartion Tool")


# Create a label to display the resulting color
color_1 = tk.Label(app, text= "______", bg = "white")
color_1.grid(row=1, column=0)
# Create a label to display the hex color code

color_2 = tk.Label(app, text= '______',  bg='white')
color_2.grid(row= 1, column = 1)

color_3 = tk.Label(app, text ='______', bg = 'white')
color_3.grid(row= 1, column= 2)


# Initialize the color display

visible_colors = tk.Label(text= "Visible Colors?")
visible_colors.grid(row=2, column=1)

#Selection of Colors Visible
left_button = tk.Button(app, text = "1 color")
left_button.grid(row = 3, column= 0)

middle_button = tk.Button(app, text = '2 colors')
middle_button.grid(row= 3, column = 1)

right_button = tk.Button(app, text = '3 colors')
right_button.grid(row= 3, column = 2)
# Start the application

#Values passed into function
l_val = 50
a_val = 0
b_val = 0
scale_val = 99

generate(l_val, a_val, b_val, scale= scale_val, type = cvd.P)
app.mainloop()
# test
import numpy as np
import random
from skimage import color
import tkinter as tk
from enum import Enum

class cvd(Enum):
    P = 11.48
    D = 8.11
    T = -46.37


def generate(l: int, a: int, b: int, scale, type: cvd):
    
    dichromat_angle = np.radians(type.value)  
    normal = np.array([0, np.cos(dichromat_angle), np.sin(dichromat_angle)])
    perpendicular_normal = np.cross(normal, np.array([1,0,0]))
    print('normal',normal)
    print('perpendicular_normal', perpendicular_normal)
    range = [scale, scale*2, 0]
    random.shuffle(range)
    print(range)
    
    
    color1 = np.array([l + 0.0, a + 0.0, b + 0.0]) + range[2] * perpendicular_normal    
    color2 = np.array([l + 0.0, a + 0.0, b + 0.0]) + range[0] * perpendicular_normal
    color3 = np.array([l + 0.0, a + 0.0, b + 0.0]) + range[1] * perpendicular_normal

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

def left_button_click():
    global scale_val 
    scale_val += 10
    generate(l_val, a_val, b_val, scale= scale_val, type = cvd.P)

def right_button_click():
    global scale_val 
    scale_val -= 10
    generate(l_val, a_val, b_val, scale= scale_val, type = cvd.P)
    
def middle_button_click():
    global l_val
    l_val += 10
    generate(l_val, a_val, b_val, scale= scale_val, type = cvd.P)




# Create the main application window
app = tk.Tk()
app.title("Calibartion Tool")


#Values passed into generate function
l_val = 50
a_val = 50
b_val = 50
scale_val = 40



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
left_button = tk.Button(app, text="1 color", command = lambda: left_button_click())
left_button.grid(row = 3, column= 0)


middle_button = tk.Button(app, text = '2 colors', command = lambda: middle_button_click())
middle_button.grid(row= 3, column = 1)

right_button = tk.Button(app, text = '3 colors', command = lambda: right_button_click())
right_button.grid(row= 3, column = 2)
# Start the application

generate(l_val, a_val, b_val, scale= scale_val, type = cvd.P)
app.mainloop()

# The main idea of this application is to find the outer bounds of a users color space.
# The user will be able to select the number of colors they can see.
# If the user can see 3 colors, the color space is too large.
# If the user can see 1 color, the color space is too small.
# If the user can see 2 colors, the color space is just right.

# The plan after this is to project all colors in a given image into the users color space.
# This will allow the user to see the colors as they would see them.

# If we can create a color palette where selecting colors that are maximally different from each other (on the edge of the color space),
# we can use k-means clustering and assign each cluster a color from the palette (customized to the user's color space).

# Should the colors scale from perpendicularly from the 2d plane? 
# Currently, the colors scale from the 2d plane. (across the slightly tilted a/b plane)
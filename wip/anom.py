import tkinter as tk
import random

def generate_random_color():
    # Generate random RGB values for the first color
    r1 = random.randint(0, 255)
    g1 = random.randint(0, 255)
    b1 = random.randint(0, 255)
    
    # Generate random RGB values for the second color
    r2 = random.randint(0, 255)
    g2 = random.randint(0, 255)
    b2 = random.randint(0, 255)
    
    # Generate random RGB values for the third color
    r3 = random.randint(0, 255)
    g3 = random.randint(0, 255)
    b3 = random.randint(0, 255)
    
    # Format colors to hexadecimal
    color1 = f'#{r1:02x}{g1:02x}{b1:02x}'
    color2 = f'#{r2:02x}{g2:02x}{b2:02x}'
    color3 = f'#{r3:02x}{g3:02x}{b3:02x}'
    
    # Update each color display
    color_display1.config(bg=color1)
    color_display2.config(bg=color2)
    color_display3.config(bg=color3)
    
    # Update labels with the RGB values
    color_value_label1.config(text=f"RGB: ({r1}, {g1}, {b1})")
    color_value_label2.config(text=f"RGB: ({r2}, {g2}, {b2})")
    color_value_label3.config(text=f"RGB: ({r3}, {g3}, {b3})")

# Create the main window
root = tk.Tk()
root.title("Random Color Generator")
root.geometry("300x600")

# Label to show the first color preview
color_display1 = tk.Label(root, text="Color 1", bg="white", width=20, height=5)
color_display1.pack(pady=10)

# Label to display the RGB values for the first color
color_value_label1 = tk.Label(root, text="RGB: (0, 0, 0)")
color_value_label1.pack(pady=5)

# Label to show the second color preview
color_display2 = tk.Label(root, text="Color 2", bg="white", width=20, height=5)
color_display2.pack(pady=10)

# Label to display the RGB values for the second color   
color_value_label2 = tk.Label(root, text="RGB: (0, 0, 0)")
color_value_label2.pack(pady=5)

# Label to show the third color preview
color_display3 = tk.Label(root, text="Target Color", bg="white", width=20, height=5)
color_display3.pack(pady=10)

# Label to display the RGB values for the third color   
color_value_label3 = tk.Label(root, text="RGB: (0, 0, 0)")
color_value_label3.pack(pady=5)

# Button to generate a new set of random colors
generate_button = tk.Button(root, text="Generate New Colors", command=generate_random_color)
generate_button.pack(pady=20)

# Buttons to pick option
color_1 = tk.Button(root, text="Color 1", command=None ) #todo: add a function to save that c1 was more close
color_1.pack(pady=10)

color_2 = tk.Button(root, text="Color 2", command =None) #todo: see above
color_2.pack(pady= 0)

cant_tell = tk.Button(root, text = 'Can\'t tell', command = None)
cant_tell.pack(pady =0)
# Generate the first set of random colors on start
generate_random_color()

# Start the GUI event loop
root.mainloop()

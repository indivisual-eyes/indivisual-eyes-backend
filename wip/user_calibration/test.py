c3 = color3 #np.array([l+.0, a+.0, b+.0])
    #convert to rgb
    c3 = color.lab2rgb(c3)
    # reformat
    c3 = np.clip((c3 * 255).astype(int), min = 0, max =255)
    # convert to hex
    c2_hex_color = f'#{c1[0]:02x}{c1[1]:02x}{c1[2]:02x}'
    # Change the color of the displayed color
    color_2.config(bg= c1_hex_color)
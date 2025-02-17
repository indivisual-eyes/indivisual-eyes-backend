import math
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from PIL import Image

min_wavelength = 400
max_wavelength = 700
steps = 1000

blue_cone_wavelength = 450
green_cone_wavelength = 529
red_cone_wavelength = 575

blue_emitter_wavelength = 450
green_emitter_wavelength = 529
red_emitter_wavelength = 575

index = lambda x: round((x - min_wavelength) / (max_wavelength - min_wavelength) * steps)
blue_index = index(blue_emitter_wavelength)
green_index = index(green_emitter_wavelength)
red_index = index(red_emitter_wavelength)


def curve(x, center, width):
    return stats.norm.pdf(x, center, width) * width * math.sqrt(2 * np.pi)


x = np.linspace(min_wavelength, max_wavelength, steps)

blue = curve(x, blue_cone_wavelength, 15)
green = curve(x, green_cone_wavelength, 27.5)
red = curve(x, red_cone_wavelength, 32.5)

blue_blue = blue[blue_index]
blue_green = blue[green_index]
blue_red = blue[red_index]

green_blue = green[blue_index]
green_green = green[green_index]
green_red = green[red_index]

red_blue = red[blue_index]
red_green = red[green_index]
red_red = red[red_index]

# ==============================================================================

fig, axs = plt.subplots(4, figsize=(5, 10))

axs[0].plot(x, blue, color='blue')
axs[0].plot(x, green, color='green')
axs[0].plot(x, red, color='red')

green_cone_slider = Slider(ax=axs[1], label='Green cone', valmin=min_wavelength, valmax=max_wavelength, valinit=green_cone_wavelength)

img = Image.open('rgb_spectrum.png')
img.load()
img = np.asarray(img, dtype=np.int16)
img2 = img.copy()

for row in range(img2.shape[0]):
    for col in range(img2.shape[1]):
        img2[row][col][2] = np.clip(np.sum([img[row][col][2] * blue_blue, img[row][col][1] * blue_green, img[row][col][0] * blue_red]), 0, 255)
        img2[row][col][1] = np.clip(np.sum([img[row][col][2] * green_blue, img[row][col][1] * green_green, img[row][col][0] * green_red]), 0, 255)
        img2[row][col][0] = np.clip(np.sum([img[row][col][2] * red_blue, img[row][col][1] * red_green, img[row][col][0] * red_red]), 0, 255)


def update(_):
    green_cone_wavelength = green_cone_slider.val
    green = curve(x, green_cone_wavelength, 27.5)
    axs[0].cla()
    axs[0].plot(x, blue, color='blue')
    axs[0].plot(x, green, color='green')
    axs[0].plot(x, red, color='red')
    green_blue = green[blue_index]
    green_green = green[green_index]
    green_red = green[red_index]

    for row in range(img2.shape[0]):
        for col in range(img2.shape[1]):
            img2[row][col][1] = np.clip(np.sum([img[row][col][2] * green_blue, img[row][col][1] * green_green, img[row][col][0] * green_red]), 0, 255)

    axs[2].imshow(img)
    axs[3].imshow(img2)
    fig.canvas.draw_idle()


green_cone_slider.on_changed(update)
update(green_cone_wavelength)

# ==============================================================================

# fig, axs = plt.subplots(6, figsize=(5, 10))
#
# axs[0].plot(x, blue, color='blue')
# axs[0].plot(x, green, color='green')
# axs[0].plot(x, red, color='red')
#
# blue_slider = Slider(ax=axs[1],label='Blue',valmin=0,valmax=1)
# green_slider = Slider(ax=axs[2],label='Green',valmin=0,valmax=1)
# red_slider = Slider(ax=axs[3],label='Red',valmin=0,valmax=1)
#
# real_color = np.zeros((1, 1, 3))
# axs[4].imshow(real_color)
#
# color = np.zeros((1, 1, 3))
# axs[5].imshow(color)
#
#
# def update(_):
#     color[0][0][2] = np.max([blue_slider.val * blue[blue_index],
#                              green_slider.val * blue[green_index],
#                              red_slider.val * blue[red_index]])
#     color[0][0][1] = np.max([blue_slider.val * green[blue_index],
#                              green_slider.val * green[green_index],
#                              red_slider.val * green[red_index]])
#     color[0][0][0] = np.max([blue_slider.val * red[blue_index],
#                              green_slider.val * red[green_index],
#                              red_slider.val * red[red_index]])
#
#     # color[0][0][2] = np.clip(
#     #     blue_slider.val * blue[blue_index]
#     #     + green_slider.val * blue[green_index]
#     #     + red_slider.val * blue[red_index], 0, 1)
#     # color[0][0][1] = np.clip(
#     #     blue_slider.val * green[blue_index]
#     #     + green_slider.val * green[green_index]
#     #     + red_slider.val * green[red_index], 0, 1)
#     # color[0][0][0] = np.clip(
#     #     blue_slider.val * red[blue_index]
#     #     + green_slider.val * red[green_index]
#     #     + red_slider.val * red[red_index], 0, 1)
#
#     real_color[0][0][2] = blue_slider.val
#     real_color[0][0][1] = green_slider.val
#     real_color[0][0][0] = red_slider.val
#
#     axs[4].imshow(real_color)
#     axs[5].imshow(color)
#
#     fig.canvas.draw_idle()
#
#
# blue_slider.on_changed(update)
# green_slider.on_changed(update)
# red_slider.on_changed(update)

plt.show()

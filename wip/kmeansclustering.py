import cv2
import numpy as np
from sklearn.cluster import KMeans

# Load the image
filename = 'wip/scatterplot.png'
image = cv2.imread(filename) #valorant_in_game000.png'

# Reshape the image to a 2D array of pixels (num_pixels, 3)
# -1 makes it to where we lose 1 dimension (aka 2 dimensions into 1)
pixels = image.reshape((-1, 3))

# Set the number of desired colors (clusters) for maximum contrast
N = 6 # This can go up to 30 (The number of colors in our palette). The number of colors used in the end image

# Apply K-means clustering to the pixels #########################
# This step allows us to find
kmeans = KMeans(n_clusters=N, random_state=13) # The higher N, the more colors, Random state is merely a SEED. It can be any number, each state corresponds with 1 exact output
kmeans.fit(pixels)


# New image using preset colors to identify color mappings#####################

# Define a palette of N maximally contrasting colors
# Example palette with 30 distinct colors, we could add more or remove some
hc_palette = np.array([
    [255, 0, 0],      # Red
    [0, 255, 0],      # Green
    [0, 0, 255],      # Blue
    [255, 255, 0],    # Yellow
    [255, 0, 255],    # Magenta
    [0, 255, 255],    # Cyan
    [128, 0, 0],      # Dark Red
    [0, 128, 0],      # Dark Green
    [0, 0, 128],      # Dark Blue
    [128, 128, 0],    # Olive
    [128, 0, 128],    # Purple
    [0, 128, 128],    # Teal
    [255, 128, 0],    # Orange
    [128, 255, 0],    # Lime
    [0, 255, 128],    # Spring Green
    [0, 128, 255],    # Light Blue
    [128, 0, 255],    # Violet
    [255, 0, 128],    # Pink
    [128, 128, 255],  # Light Purple
    [255, 128, 128],  # Light Red
    [128, 255, 128],  # Light Green
    [128, 128, 128],  # Gray
    [192, 192, 192],  # Silver
    [64, 64, 64],     # Dark Gray
    [255, 192, 0],    # Gold
    [192, 64, 0],     # Dark Orange
    [0, 64, 192],     # Royal Blue
    [64, 0, 192],     # Indigo
    [192, 0, 64],     # Crimson
    [0, 192, 64]      # Sea Green
], dtype=np.uint8)

d_palette = np.array([
    (0, 0, 128),      # Navy Blue
    (255, 215, 0),    # Gold
    (75, 0, 130),     # Indigo
    (255, 140, 0),    # Dark Orange
    (0, 191, 255),    # Deep Sky Blue
    (220, 20, 60),    # Crimson
    (255, 255, 0),    # Yellow
    (0, 0, 205),      # Medium Blue
    (138, 43, 226),   # Blue Violet
    (245, 222, 179),  # Wheat
    (128, 0, 128),    # Purple
    (218, 165, 32),   # Goldenrod
    (47, 79, 79),     # Dark Slate Gray
    (240, 128, 128),  # Light Coral
    (0, 128, 128)     # Teal
], dtype =np.uint8)

t_palette = np.array([
    (139, 0, 0),       # Dark Red
    (34, 139, 34),     # Forest Green
    (178, 34, 34),     # Firebrick
    (154, 205, 50),    # Yellow Green
    (128, 0, 128),     # Purple
    (255, 165, 0),     # Orange
    (105, 105, 105),   # Dim Gray
    (189, 183, 107),   # Dark Khaki
    (210, 105, 30),    # Chocolate
    (50, 205, 50),     # Lime Green
    (255, 20, 147),    # Deep Pink
    (85, 107, 47),     # Dark Olive Green
    (244, 164, 96),    # Sandy Brown
    (128, 128, 0),     # Olive
    (205, 133, 63)     # Peru
], dtype =np.uint8)

p_palette = np.array([
    (0, 0, 128),      # Navy Blue
    (255, 215, 0),    # Gold
    (0, 128, 0),      # Green
    (255, 140, 0),    # Dark Orange
    (0, 191, 255),    # Deep Sky Blue
    (128, 0, 128),    # Purple
    (255, 255, 0),    # Yellow
    (0, 0, 205),      # Medium Blue
    (138, 43, 226),   # Blue Violet
    (245, 222, 179),  # Wheat
    (47, 79, 79),     # Dark Slate Gray
    (240, 230, 140),  # Khaki
    (0, 139, 139),    # Dark Cyan
    (100, 149, 237),  # Cornflower Blue
    (210, 180, 140)   # Tan
], dtype = np.uint8
)

# Initialize an empty array
mono_palette = np.empty((0, 3),dtype=np.uint8) # you cannot set this as datatype=np.uint8 for some god-forsaken reason. 
# That's why we have pre and nomral

# Initialize the starting value and the decrement factor
cur = 255    
n_factor = int(255 / N)

# Loop to generate greyscale colors
while cur >= 0 + n_factor:
    mono_palette = np.vstack([mono_palette, (cur, cur, cur)])  # Append to the array
    cur -= n_factor

mono_palette[N-1] = (0, 0, 0)
mono_palette = mono_palette.astype(np.uint8)




# Change this line to filter <------------------------------------------------------------------------------------------------------
palette = mono_palette
str(hc_palette)

# Map each pixel's cluster to the corresponding color from the palette
labels = kmeans.labels_  # Get the cluster labels for each pixel.
# This takes the kmeans results and assigns an identifier with a cluster (our N value)
new_pixels = palette[labels]  # Replace each pixel with its cluster's palette color

# Reshape the new_pixels array to match the original image shape
filtered_image = new_pixels.reshape(image.shape)


# New image using the original colors ########################
new_colors = kmeans.cluster_centers_[kmeans.predict(pixels)]
reduced_color = new_colors.reshape(image.shape).astype(np.uint8)

# Display the original and the high-contrast recolored image
cv2.imshow('Original Image', image)
cv2.imshow('Filtered Image', filtered_image)
# cv2.imshow('kmeans Image [N colors]', reduced_color)



# Save new images
# cv2.imwrite(str(filename)+'filtered'+'.jpg' , filtered_image)


# Wait for a key press and close the windows
cv2.waitKey(0)
cv2.destroyAllWindows()

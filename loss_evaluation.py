import cv2
import numpy as np
from skspatial.objects import Plane, Vector
from scipy.spatial.transform import Rotation as R
import matplotlib.pyplot as plt
import random as 

def evaluate(iterations:int, image: cv2.typing.MatLike, p_image: cv2.typing.MatLike):
    height, width = image.shape[0], image.shape[1]
    # We are finding the maximum distance that two pixels can be apart from one another
    max_distance = (2/np.pi)(np.sqrt(2* min(height, width))) 
    for i in range(iterations):
        r_height = random.randrange(0,height-1)
        r_width = random.randrange(0, width-1)
        while (r_height)
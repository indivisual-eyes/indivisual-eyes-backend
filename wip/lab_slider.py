import colorspacious as cs
import cv2
image = cv2.imread('wip/test_photos/machado.png')

converted = cs.cspace_convert(image, "sRGB255", "XYZ100")
print(converted)
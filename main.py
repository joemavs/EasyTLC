import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import tkinter as tk
from skimage.io import imread
import cv2
from skimage import exposure
from skimage.feature import canny
from math import atan2, degrees

imageObj = Image.open('images/tlc_2.jpg')
plt.imshow(imageObj)
plt.draw()
solvent_front = np.array(plt.ginput(1, 0, True)) # Get line from user input
sf_y_axis = solvent_front.flatten()[1]
print(sf_y_axis)
plt.axhline(y=sf_y_axis, color='red', linestyle='--', linewidth=2)
plt.show()







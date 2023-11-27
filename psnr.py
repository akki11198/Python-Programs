import math
import cv2
import numpy as np

def psnr(x,y):
    for i in range (500):
        mse = np.mean((x - y) ** 2)
        if mse == 0:
            return 100
        PIXEL_MAX = 255.0
        return 20 * math.log10(PIXEL_MAX / math.sqrt(mse))



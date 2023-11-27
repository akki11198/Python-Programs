# let's start with the Imports
# let's start with the Imports
import cv2
import numpy as np
from tqdm import tqdm
# Set up the image source and destination foldername
srcfoldername = 'D:\\Datasets\\Pascal VOC (128x128)\\train\\set30\\images\\'
#destfoldername = 'D:\\Python Programs\\Datasets\\pscl\\test\\images\\'
destfoldername = 'D:\\Datasets\\Pascal VOC (256x256)\\train\\set30\\images\\'
# Set up total number of images
total = 368
x = 13671
# Set the loop and progress bar
for i in tqdm(range(total)):
    # Setup the image filename
    filename = str(x).zfill(5)+'.JPEG'
    # Read the image using imread function
    image = cv2.imread(srcfoldername+filename)
    # let's downscale the image using new  width and height
    down_width = 256
    down_height = 256
    down_points = (down_width, down_height)
    resized_down = cv2.resize(image, down_points, interpolation=cv2.INTER_CUBIC)
    # Write the image using imwrite function
    cv2.imwrite(destfoldername+filename, resized_down)
    x = x+1

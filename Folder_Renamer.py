import os
from functools import partial
_dir = 'D:\\Python Programs\\Datasets\\VOC Pascal\\'
folder = os.listdir(_dir)
i = 0
folder = (d for d in os.listdir(_dir))
for fn in folder:
    for ind, fn in enumerate(folder, 1):
        os.rename(os.path.join(_dir, fn), os.path.join(_dir,  str(i).zfill(5) + '.JPEG'))
        i += 1
        

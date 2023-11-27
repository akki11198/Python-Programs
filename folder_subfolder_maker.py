import os
from functools import partial

root_directory = 'D:\\Datasets\\Pascal VOC (256x256)\\train'
list = []
for i in range(30):
    strng = 'set' + str(i+1) + '/images'
    list.append(strng)

concat_root_path = partial(os.path.join, root_directory)
make_directory = partial(os.makedirs, exist_ok=True)

for path_items in map(concat_root_path, list):
    make_directory(path_items)

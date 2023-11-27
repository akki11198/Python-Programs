import os
import shutil
import random
import pandas as pd
import torch
from torchvision import transforms
from PIL import Image

dataset_dir = 'D:\Python Programs\Datasets\imagenette2-320\Train'
dataset_folder = 'Set'
dataset_path = os.path.join(dataset_dir, dataset_folder)
training_folder_dir = 'D:\Python Programs\Datasets\DS_Train'


def delete_image(image_path):
    if '.txt' in image_path:
        os.remove(image_path)
        return

    img = Image.open(image_path)
    img_shape = transforms.ToTensor()(img).size()
    if img_shape[0] == 1:
        os.remove(image_path)


if not os.path.exists(dataset_path):
    os.makedirs(dataset_path)


for i, folder in enumerate(os.listdir(training_folder_dir)):
    files = os.listdir(os.path.join(training_folder_dir, folder, 'images'))

    for _file in files:
        delete_image(os.path.join(
            training_folder_dir, folder, 'images', _file))

    selected_files = random.sample(files, 14)
    validation_images, train_images = selected_files[:4], selected_files[4:]
    for image in train_images:
        shutil.copyfile(os.path.join(training_folder_dir, folder,
                        'images', image), os.path.join(dataset_path, 'train', image))
    for image in validation_images:
        shutil.copyfile(os.path.join(training_folder_dir, folder,
                        'images', image), os.path.join(dataset_path, 'valid', image))


training_images = os.listdir(os.path.join(dataset_path, 'train'))
random.shuffle(training_images)

cover_images = training_images[:240]
secret_images_1 = training_images[240:480]
secret_images_2 = training_images[480:720]
secret_images_3 = training_images[720:]

dataset = []
for i in range(240):
    dataset.append({
        'cover_image': cover_images[i],
        'secret_image_1': secret_images_1[i],
        'secret_image_2': secret_images_2[i],
        'secret_image_3': secret_images_3[i]
    })

dataframe = pd.DataFrame(dataset)
dataframe.to_csv('D:\Python Programs\Datasets\Train_dataset.csv')

validation_images = os.listdir(os.path.join(dataset_path, 'valid'))
random.shuffle(validation_images)

cover_images = validation_images[:97]
secret_images_1 = validation_images[97:194]
secret_images_2 = validation_images[194:291]
secret_images_3 = validation_images[291:]

dataset = []
for i in range(97):
    dataset.append({
        'cover_image': cover_images[i],
        'secret_image_1': secret_images_1[i],
        'secret_image_2': secret_images_2[i],
        'secret_image_3': secret_images_3[i]
    })

dataframe = pd.DataFrame(dataset)
dataframe.to_csv('D:\Python Programs\Datasets\Validation_dataset.csv')

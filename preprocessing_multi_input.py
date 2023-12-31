# -*- coding: utf-8 -*-
"""preprocessing_multi_input.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WtUuKD_GMAAhRjPW8eNw0vf6uvKO-J9t
"""

#!/usr/bin/python3

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision.models import resnet50
from torchvision.transforms import ToTensor
from torch.autograd import Variable
import torch.utils.data as data
from PIL import Image
import natsort
import os
import sys
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import cv2
import pywt
import shutil
import sklearn.model_selection as sk
from torch.utils.data import DataLoader, TensorDataset
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from torchvision import transforms, models
from torchvision import utils
# from torchsummary import summary
# from torchsummaryX import summary

import pretrainedmodels
# import timm
from PIL import Image, ImageFilter

#from google.colab import drive
#drive.mount('/content/drive')

# Dataset path load
train_path = '../../test_set'  # train_set image 경로

def preprocess_image(img):
  color_image = np.array(img)
  grayscale_image = img.convert("L")
  grayscale_image = np.array(grayscale_image)
  threshold_min=130
  threshold_max=255

  # canny = cv2.Canny(img, 500, 700) # 처리할 이미지 사진 / min Threshold / max Threshold
  # #blurred = cv2.blur(img, (25, 25))  # 주변 값으로 대체하기 위해 이미지 블러링 수행


  # result = np.where(canny != 0, img, dst)
  canny = cv2.Canny(grayscale_image, 500, 700)  # Canny 엣지 검출
  blurred_edges = cv2.blur(canny, (17, 17))  # 엣지 영역을 블러링하여 부드럽게 처리
  blurred_image = cv2.blur(grayscale_image, (17, 17))  # 이미지 전체를 블러링하여 주변 값으로 대체할 대상 생성

  result = np.where(canny != 0, grayscale_image, blurred_image)
  _, binary_image = cv2.threshold(result, threshold_min, threshold_max, cv2.THRESH_BINARY)
  contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

  max_contour = max(contours, key=cv2.contourArea)
  x, y, w, h = cv2.boundingRect(max_contour)
  margin = 15

  cropped_image = color_image[y+margin:y+h-margin, x+margin:x+w-margin]

# 8개의 폴더 생성
os.makedirs('../../test_set_LI-A')
os.makedirs('../../test_set_LI-B')
os.makedirs('../../test_set_LV-A')
os.makedirs('../../test_set_LV-B')
os.makedirs('../../test_set_RI-A')
os.makedirs('../../test_set_RI-B')
os.makedirs('../../test_set_RV-A')
os.makedirs('../../test_set_RV-B')

# 각각 경로 설정
LI_A_path = '../../test_set_LI-A'
LI_B_path = '../../test_set_LI-B'
LV_A_path = '../../test_set_LV-A'
LV_B_path = '../../test_set_LV-B'
RI_A_path = '../../test_set_RI-A'
RI_B_path = '../../test_set_RI-B'
RV_A_path = '../../test_set_RV-A'
RV_B_path = '../../test_set_RV-B'

# 이미지를 클래스별로 분류하고 저장
print("checkpoint: no error")

for filename in os.listdir(train_path):
    source_path = os.path.join(train_path, filename)

    if 'LI-A' in filename:
        destination_path = os.path.join(LI_A_path, filename)
    elif 'LI-B' in filename:
        destination_path = os.path.join(LI_B_path, filename)
    elif 'LV-A' in filename:
        destination_path = os.path.join(LV_A_path, filename)
    elif 'LV-B' in filename:
        destination_path = os.path.join(LV_B_path, filename)
    elif 'RI-A' in filename:
        destination_path = os.path.join(RI_A_path, filename)
    elif 'RI-B' in filename:
        destination_path = os.path.join(RI_B_path, filename)
    elif 'RV-A' in filename:
        destination_path = os.path.join(RV_A_path, filename)
    elif 'RV-B' in filename:
        destination_path = os.path.join(RV_B_path, filename)
    else:
        continue

    img = Image.open(source_path)
    cropped_image = preprocess_image(img)

    # If cropped_image is None, save the original image
    if cropped_image is None:
        shutil.copy(source_path, destination_path)
    else:
        cropped_img_pil = Image.fromarray(cropped_image)
        cropped_img_pil.save(destination_path)

print("Image classification and saving completed.")

# 폴더 별 이미지 (100,100)으로 resize
IMG_SIZE = 100
data = []
classes = ['yes', 'no']

files = natsort.natsorted(os.listdir(LI_A_path))
for f in files:
    img = Image.open(LI_A_path + '/' + f)

    # 이미지 리사이즈
    img = img.resize((IMG_SIZE, IMG_SIZE))

    one_img = np.asarray(np.float32(img))
    norm_img = one_img / 255.0

    img = np.asarray([norm_img])
    data.append(img)

data1 = np.array(data, dtype='float32')

data = []
classes = ['yes', 'no']

files = natsort.natsorted(os.listdir(LI_B_path))
for f in files:
    img = Image.open(LI_B_path + '/' + f)

    # 이미지 리사이즈
    img = img.resize((IMG_SIZE, IMG_SIZE))

    one_img = np.asarray(np.float32(img))
    norm_img = one_img / 255.0

    img = np.asarray([norm_img])
    data.append(img)

data2 = np.array(data, dtype='float32')

data = []
classes = ['yes', 'no']

files = natsort.natsorted(os.listdir(LV_A_path))
for f in files:
    img = Image.open(LV_A_path + '/' + f)

    # 이미지 리사이즈
    img = img.resize((IMG_SIZE, IMG_SIZE))

    one_img = np.asarray(np.float32(img))
    norm_img = one_img / 255.0

    img = np.asarray([norm_img])
    data.append(img)

data3 = np.array(data, dtype='float32')

data = []
classes = ['yes', 'no']

files = natsort.natsorted(os.listdir(LV_B_path))
for f in files:
    img = Image.open(LV_B_path + '/' + f)

    # 이미지 리사이즈
    img = img.resize((IMG_SIZE, IMG_SIZE))

    one_img = np.asarray(np.float32(img))
    norm_img = one_img / 255.0

    img = np.asarray([norm_img])
    data.append(img)

data4 = np.array(data, dtype='float32')

data = []
classes = ['yes', 'no']

files = natsort.natsorted(os.listdir(RI_A_path))
for f in files:
    img = Image.open(RI_A_path + '/' + f)

    # 이미지 리사이즈
    img = img.resize((IMG_SIZE, IMG_SIZE))

    one_img = np.asarray(np.float32(img))
    norm_img = one_img / 255.0

    img = np.asarray([norm_img])
    data.append(img)

data5 = np.array(data, dtype='float32')

data = []
classes = ['yes', 'no']

files = natsort.natsorted(os.listdir(RI_B_path))
for f in files:
    img = Image.open(RI_B_path + '/' + f)

    # 이미지 리사이즈
    img = img.resize((IMG_SIZE, IMG_SIZE))

    one_img = np.asarray(np.float32(img))
    norm_img = one_img / 255.0

    img = np.asarray([norm_img])
    data.append(img)

data6 = np.array(data, dtype='float32')

data = []
classes = ['yes', 'no']

files = natsort.natsorted(os.listdir(RV_A_path))
for f in files:
    img = Image.open(RV_A_path + '/' + f)

    # 이미지 리사이즈
    img = img.resize((IMG_SIZE, IMG_SIZE))

    one_img = np.asarray(np.float32(img))
    norm_img = one_img / 255.0

    img = np.asarray([norm_img])
    data.append(img)

data7 = np.array(data, dtype='float32')

data = []
classes = ['yes', 'no']

files = natsort.natsorted(os.listdir(RV_B_path))
for f in files:
    img = Image.open(RV_B_path + '/' + f)

    # 이미지 리사이즈
    img = img.resize((IMG_SIZE, IMG_SIZE))

    one_img = np.asarray(np.float32(img))
    norm_img = one_img / 255.0

    img = np.asarray([norm_img])
    data.append(img)

data8 = np.array(data, dtype='float32')
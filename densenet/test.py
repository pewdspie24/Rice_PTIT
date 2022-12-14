import os

import tensorflow as tf
from tensorflow.keras.applications import (
    MobileNetV2,
    VGG16,
    MobileNetV3Large,
    ResNet50,
    ResNet50V2,
    DenseNet121,
)

# from classification_models.tfkeras import Classifiers
from tensorflow.keras.callbacks import CSVLogger
from tensorflow.keras.applications.efficientnet import EfficientNetB0
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.layers import (
    Input,
    Flatten,
    Dense,
    Dropout,
    Permute,
    Reshape,
    GlobalAveragePooling2D,
    AveragePooling2D,
    BatchNormalization,
    Activation,
)
from tensorflow.keras.models import Model
import numpy as np
from imutils import paths
import matplotlib.pyplot as plt
from tensorflow.keras.optimizers import SGD, Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.utils import class_weight
from PIL import Image
import tensorflow
import cv2
from sklearn.metrics import f1_score

reconstructed_model = tensorflow.keras.models.load_model(r"model\rice\densenet_end.h5")
truth = []
predict = []
for file in os.listdir("valid/BrownSpot"):
    img = cv2.imread("valid/BrownSpot/"+file)
    img = cv2.resize(img, (224,224))
    img = np.expand_dims(img, axis=0)
    # print(img.shape)
    pred = reconstructed_model.predict(img, batch_size = 1)
    predict.append(np.argmax(pred).item())
    print(np.argmax(pred).item())
    truth.append(0)
print("c")
for file in os.listdir("valid/Healthy"):
    img = cv2.imread("valid/Healthy/"+file)
    img = cv2.resize(img, (224,224))
    img = np.expand_dims(img, axis=0)
    # print(img.shape)
    pred = reconstructed_model.predict(img, batch_size = 1)
    predict.append(np.argmax(pred).item())
    truth.append(1)

for file in os.listdir("valid/Hispa"):
    img = cv2.imread("valid/Hispa/"+file)
    img = cv2.resize(img, (224,224))
    img = np.expand_dims(img, axis=0)
    # print(img.shape)
    pred = reconstructed_model.predict(img, batch_size = 1)
    predict.append(np.argmax(pred).item())
    print(np.argmax(pred).item())
    truth.append(2)

for file in os.listdir("valid/LeafBlast"):
    img = cv2.imread("valid/LeafBlast/"+file)
    img = cv2.resize(img, (224,224))
    img = np.expand_dims(img, axis=0)
    # print(img.shape)
    pred = reconstructed_model.predict(img, batch_size = 1)
    predict.append(np.argmax(pred).item())
    print(np.argmax(pred).item())
    truth.append(3)

# average=None: calculate f1_sorce for each label, average!=None: calculate f1_sorce all
with open(r'a.txt', 'w') as fp:
    fp.write("PREDICT\n")
    for item in predict:
        # write each item on a new line
        fp.write("%s " % str(item))
    fp.write("\nTRUTH\n")
    for item in truth:
        # write each item on a new line
        fp.write("%s " % str(item))
    print('Done')

print("pre_concat: ", f1_score(truth, predict, average=None), f1_score(truth, predict, average='macro'))
print("pre_combine: ", f1_score(truth, predict, average=None), f1_score(truth, predict, average='macro'))
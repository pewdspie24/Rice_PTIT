from PIL import Image
import os
import tensorflow as tf
import cv2
import numpy as np
from tensorflow.keras.applications import InceptionV3
from tensorflow.keras.layers import (
    Input,
    Dense,
    Dropout,
    GlobalAveragePooling2D,
    BatchNormalization,
    Activation,
)
from tensorflow.keras.models import Model
from tensorflow.keras.utils import get_custom_objects
import io
import sys

sys.path.append("Data_Collector_API/models")
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
# Mish Activation


class Mish(Activation):
    def __init__(self, activation, **kwargs):
        super(Mish, self).__init__(activation, **kwargs)
        self.__name__ = 'Mish'


def mish(inputs):
    return inputs * tf.math.tanh(tf.math.softplus(inputs))


get_custom_objects().update({'Mish': Mish(mish)})


class ModelPredict:
    def __init__(self, model_path="/home/riceleaf/rice/Rice_PTIT/Data_Collector_API/models/299x299_ver2_prebest.h5"):
        self.model = self.load_model_architecture()
        self.model.load_weights(model_path)

    def load_model_architecture(self):
        model_raw = InceptionV3(
            include_top=False,
            weights='imagenet',
            input_tensor=Input(shape=(299, 299, 3)),
        )

        headModel = model_raw.output

        feed_x = GlobalAveragePooling2D()(headModel)
        feed_x = BatchNormalization()(feed_x)
        feed_x = Dropout(0.5)(feed_x)
        feed_x = Dense(1024, activation="Mish")(feed_x)
        feed_x = Dense(512, activation="Mish")(feed_x)
        feed_x = BatchNormalization()(feed_x)
        feed_x = Dropout(0.5)(feed_x)
        preds = Dense(4, activation="softmax")(feed_x)

        model = Model(inputs=model_raw.input, outputs=preds)

        model_raw.trainable = True
        fine_tune_at = 120
        for layer in model_raw.layers[:fine_tune_at]:
            layer.trainable = False

        # model.summary()
        return model

    def predict(self, img_bytes):
        # 'brownSpot': 0, 'healthy': 1, 'hispa': 2, 'leafblast': 3

        tensor = self.transform_image(img_bytes)
        predict = self.model(tensor)
        label_pre = np.argmax(predict)
        return label_pre

    def predict_percent(self, img_bytes):
        # 'brownSpot': 0, 'healthy': 1, 'hispa': 2, 'leafblast': 3

        tensor = self.transform_image(img_bytes)
        predict = self.model(tensor)
        return predict

    def transform_image(self, image_bytes):
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        img_resized = img.resize((299, 299))
        return np.expand_dims(img_resized, 0)

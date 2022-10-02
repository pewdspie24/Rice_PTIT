import cv2
from PIL import Image
import io
import sys
import math
import numpy as np
sys.path.append("Data_Collector_API/models")


class Processor:
    def __init__(self, img_bytes):
        self.img = Image.open(io.BytesIO(img_bytes)).convert('RGB')
        # self.img = Image.open(img_bytes).convert('RGB')
        self.img = self.img.resize((550, 550))
        self.img = np.array(self.img)
        self.img = self.img[:, :, ::-1].copy()
        # self.blur_threshold = 1315.0 - 600  # mean of new data
        self.blur_threshold = 200.0
        self.bright_threshold = 130.0
        self.state = {
            # "{blur}{bright}" = {state}
            "11": -3,    # blurry and high-light
            '1-1': -4,    # blurry and low-light
            '10': -2,    # blurry
            '01': -1,    # high-light
            '0-1': 0,     # low-light
            '00': 1      # OK
        }

    def Init(self, path):
        self.img = Image.open(path).convert('RGB')
        self.img = self.img.resize((550, 550))
        self.img = np.array(self.img)
        self.img = self.img[:, :, ::-1].copy()

    def check_blur(self):
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        print("blur thresh: ", cv2.Laplacian(gray, cv2.CV_64F).var())
        if cv2.Laplacian(gray, cv2.CV_64F).var() < self.blur_threshold:
            return True
        return False

    def get_blur_prop(self, lst=[]):
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        lst.append(cv2.Laplacian(gray, cv2.CV_64F).var())

    def get_pixel_brightness(self, pixel):
        assert 3 == len(pixel)
        r, g, b = pixel
        return math.sqrt(0.299 * r ** 2 + 0.587 * g ** 2 + 0.114 * b ** 2)

    def check_brightness(self):
        nr_of_pixels = len(self.img) * len(self.img[0])
        brightness = 0
        for row in self.img:
            for pixel in row:
                brightness += self.get_pixel_brightness(pixel)
        brightness /= nr_of_pixels
        # brightness = sum(self.get_pixel_brightness(pixel)
        #                  for pixel in row for row in self.img) / nr_of_pixels
        print("bright: ", brightness)
        if brightness > (self.bright_threshold + self.bright_threshold / 4):
            return 1
        if brightness < (self.bright_threshold - self.bright_threshold / 4):
            return -1
        return 0

    def process(self):
        blur = 0 if self.check_blur() == False else 1
        bright = self.check_brightness()
        s_state = str(blur) + str(bright)
        return self.state[s_state]


if __name__ == "__main__":
    import glob
    import natsort
    import os
    root = r"G:\CodeStuff\Rice_PTIT\new_data\\**\*"
    files2 = glob.glob(root, recursive=True)
    files2 = natsort.natsorted(files2, reverse=False)
    blur = []
    bright = []
    ite = 0
    processor = Processor()
    import tqdm
    for file in tqdm.tqdm(files2):
        try:
            a = file.replace("\\", "/")
            if os.path.isdir(file):
                continue
            # print("processing")
            processor.Init(a)
            processor.get_blur_prop(blur)
            bright.append(processor.check_brightness())
        except:
            print(file)
    mean_blur = sum(blur) / len(blur)
    mean_bright = sum(bright) / len(bright)

    print(mean_blur)
    print(mean_bright)

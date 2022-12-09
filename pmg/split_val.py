import glob
import os
import shutil
import random

for folder in os.listdir("new_data"):
    os.makedirs("dataset/" + folder)
    files = glob.glob(os.path.join("new_data", folder) + "/*")
    files_len = len(files)
    random.shuffle(files)
    for idx, img in enumerate(files):
        if os.path.isfile(img):
            shutil.move(img, os.path.join("dataset/" + folder, os.path.basename(img)))
            if idx == files_len // 5:
                break

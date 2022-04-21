from process_data import process
from cProfile import label
import torch
from torch.utils.data import dataset
from torchvision.transforms import transforms
import torch.utils.data as data
from PIL import Image
from torchvision.io import read_image
import numpy as np
import pandas as pd
import os

DATA_ROOT = ""


class CustomDataset(data.Dataset):
    def __init__(self, type="train") -> None:
        super(CustomDataset, self).__init__()
        # self.labels = pd.get_dummies(self.df["category"]).as_matrix()
        self.height = 224
        self.width = 224
        self.mode = type
        if self.mode == "train":
            self.DATA_DIR = os.path.join(DATA_ROOT, "train")
            self.df = process()
        else:
            self.DATA_DIR = os.path.join(DATA_ROOT, "validation")
            self.df = process("validation")

    def img_transform(self, img):
        train_transform = transforms.Compose([
            # transforms.RandomAffine(degrees=10),
            transforms.Resize(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
        val_transform = transforms.Compose([
            transforms.Resize(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

        if self.mode == "train":
            img = train_transform(img)
        else:
            img = val_transform(img)
        return img

    def __getitem__(self, index):
        filePath = self.df.iloc[index]['filepath'].replace("\\", "\\\\")
        img = Image.open(str(filePath))
        label = self.df.iloc[index]['category']
        img = self.img_transform(img)
        return img, torch.tensor(label).to(torch.long)

    def __len__(self):
        return len(self.df)


def test_transform(img):
    train_transform = transforms.Compose([
        transforms.RandomAffine(degrees=10),
        transforms.Resize(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    img = train_transform(img)
    return img


if __name__ == "__main__":
    a = CustomDataset()
    print(torch.tensor(a.df.iloc[3273]['category']).to(torch.long))
    img, label = a.__getitem__(3273)
    img.show()

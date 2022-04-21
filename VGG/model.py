from platform import release
from turtle import forward
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchinfo import summary
from torchvision import models

class VGG16(nn.Module):
    def __init__(self, num_classes=4, mode="train") -> None:
        super(VGG16, self).__init__()
        self.mode = mode
        self.ConvBlock = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 64, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(128, 128, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(256, 512, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(512, 512, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(512, 512, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(512, 512, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(512, 512, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(512, 512, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )

        self.FullyConnected = nn.Sequential(
            nn.Linear(7 * 7 * 512, 4096),
            # nn.Linear(22 * 22 * 512, 4096), #mod for unchange img size
            nn.ReLU(inplace=True),
            nn.Linear(4096, 4096),
            nn.ReLU(inplace=True),
            nn.Linear(4096, num_classes),
            # nn.Softmax(dim=1)
        )

    def forward(self, x):
        x = self.ConvBlock(x)
        x = x.view(-1, 7 * 7 * 512)
        x = self.FullyConnected(x)
        return x

    def vgg16(self):
        x = nn.Sequential(
            self.ConvBlock,
            nn.Flatten(),
            self.FullyConnected
        )
        return x

    def _summary(self):
        print(summary(self.vgg16.classifier))

class VGG16_pretrained(nn.Module):
    def __init__(self, num_classes=4) -> None:
        super(VGG16_pretrained, self).__init__()
        self.vgg16 = models.vgg16(pretrained=True)
        self.vgg16.classifier[6] = nn.Linear(4096, num_classes)

    def forward(self, x):
        return self.vgg16(x)

    def _summary(self):
        print(summary(self.vgg16.classifier))

if __name__ == "__main__":
    x = VGG16().vgg16()
    # print(summary(x.children))
    x._summary()

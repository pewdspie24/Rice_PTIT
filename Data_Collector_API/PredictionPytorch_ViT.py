from PIL import Image
import io

import torch
import timm
import torch.nn as nn
import torchvision.transforms as transforms
import sys

sys.path.append("Data_Collector_API/models")

class ViTBase16(nn.Module):
  def __init__(self, n_classes):
    super(ViTBase16, self).__init__()

    self.model = timm.create_model("vit_base_patch16_224", pretrained=False)
    self.model.head = nn.Linear(self.model.head.in_features, n_classes)

  def forward(self, x):
    x = self.model(x)
    return x

class Compose():
  def __init__(self, transforms):
    self.transforms = transforms

  def __call__(self, img):
    for t in self.transforms:
      img = t(img)
    return img

class Resize():
  def __init__(self, size):
    self.size = size

  def __call__(self, img):
    img = img.resize((self.size, self.size), Image.BILINEAR)
    return img

class Normalize_Tensor():
  def __init__(self, mean, std):
    self.mean = mean
    self.std = std

  def __call__(self, img):
    img = transforms.functional.to_tensor(img)
    img = transforms.functional.normalize(img, self.mean, self.std)
    return img

class ModelPredict:
    def __init__(self, device="cuda", model_path="models/ViT_244x244_16.pth"):
        self.device = torch.device(device=device)
        self.model = ViTBase16(n_classes=4)
        self.model.load_state_dict(torch.load(model_path))
        self.model.to(device)
        self.model.eval()

    def predict(self, img_bytes):
        tensor = self.transform_image(img_bytes).to(self.device)
        outputs = self.model(tensor)
        return torch.max(outputs.data, 1)[1].item()

    def predict_percent(self, img_bytes):
        tensor = self.transform_image(img_bytes).to(self.device)
        outputs = self.model(tensor)
        return torch.softmax(outputs.squeeze(), dim=0)

    def transform_image(self, image_bytes):
        color_mean = (0.485, 0.456, 0.406)
        color_std = (0.229, 0.224, 0.225)
        my_transforms = Compose(
            [
                Resize(size=224),
                Normalize_Tensor(mean = color_mean, std = color_std),
            ]
        )

        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        return my_transforms(image).unsqueeze(0)

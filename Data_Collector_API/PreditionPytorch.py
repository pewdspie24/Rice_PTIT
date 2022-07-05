from PIL import Image
import io

import torch
import torchvision.transforms as transforms


class ModelPredict:
    def __init__(self, device="cuda", model_path="models/model.pth"):
        self.device = torch.device(device=device)
        self.model = torch.load(model_path)
        self.model.to(self.device)
        self.model.eval()

    def predict(self, img_bytes):
        tensor = self.transform_image(img_bytes).to(self.device)
        outputs = self.model.forward(tensor)
        return outputs

    def transform_image(self, image_bytes):
        my_transforms = transforms.Compose(
            [
                transforms.Scale((550, 550)),
                transforms.RandomCrop(448, padding=8),
                transforms.RandomHorizontalFlip(),
                transforms.ToTensor(),
                transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
            ]
        )
        image = Image.open(io.BytesIO(image_bytes))
        return my_transforms(image).unsqueeze(0)

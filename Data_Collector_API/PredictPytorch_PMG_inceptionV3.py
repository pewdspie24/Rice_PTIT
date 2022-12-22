from PIL import Image
import io

import torch
import torchvision.transforms as transforms
import sys

sys.path.append("Data_Collector_API/models")


class ModelPredict:
    def __init__(self, device="cuda", model_path="model_cub_inception.pth"):
        self.device = torch.device(device=device)
        self.model = torch.load(model_path, map_location=self.device)
        self.model.eval()

    def predict(self, img_bytes):
        tensor = self.transform_image(img_bytes).to(self.device)
        with torch.no_grad():
            output_1, output_2, output_3, output_concat = self.model.forward(tensor)
        outputs_com = output_1 + output_2 + output_3 + output_concat
        _, predicted_com = torch.max(outputs_com.data, 1)
        return predicted_com.item()

    def predict_percent(self, img_bytes):
        tensor = self.transform_image(img_bytes).to(self.device)
        output_1, output_2, output_3, output_concat = self.model.forward(tensor)
        outputs_com = output_1 + output_2 + output_3 + output_concat
        predicted_com = torch.softmax(outputs_com.squeeze(), dim=0)
        return predicted_com

    def transform_image(self, image_bytes):
        my_transforms = transforms.Compose(
            [
                transforms.Resize((448, 448)),
                transforms.ToTensor(),
                transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
            ]
        )
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        return my_transforms(image).unsqueeze(0)

import os
import sys
import PredictionPytorch_ViT

sys.path.append("Data_Collector_API/models")
print(os.path.exists('models/ViT_244x244_16.pth'))

model = PredictionPytorch_ViT.ModelPredict()
print(model.model)
import os
import time
from datetime import datetime
from PIL import Image

import flask
import json
from flask import request, render_template
from flask.helpers import make_response
from werkzeug.utils import secure_filename

# import PredictionPytorch
import PreProcessor
# import PredictionTensor
import PredictionPytorch_ViT

app = flask.Flask(__name__)
# app.config["DEBUG"] = True

cwd = os.getcwd()
# cwd = os.path.join(cwd, "Data_Collector_API")

# FOR TENSOR
# classifier = PredictionTensor.ModelPredict(
#     model_path=os.path.join("/home/riceleaf/rice/Rice_PTIT/Data_Collector_API/models/299x299_ver2_prebest.h5")
# )

# FOR TORCH
classifier = PredictionPytorch_ViT.ModelPredict(
    model_path=os.path.join(os.path.join(cwd, "models"), "ViT_244x244_16.pth")
)

class_name = {0: "BrownSpot", 1: "Healthy", 2: "Hispa", 3: "LeafBlast"}


def listToString(s):

    # initialize an empty string
    str1 = ""

    # traverse in the string
    for ele in s:
        str1 += str(ele)

    # return string
    return str1


@app.route("/")
def hello():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    file = request.files["file"]
    byte_file = file.read()
    output = classifier.predict(byte_file)
    response = make_response(class_name.get(output))
    return response


@app.route("/send2server", methods=["POST"])
def get_img():
    import io
    import numpy as np
    buffer = io.BytesIO()
    file = request.files["file"]
    byte_file = file.read()
    file.save(buffer)
    image = np.array(Image.open(file, formats=["JPEG"]))
    image = Image.fromarray(image)
    processor = PreProcessor.Processor(byte_file)
    result = processor.process()
    if result == 1:
        outputs = classifier.predict_percent(byte_file)
        result = []
        # FOR PYTORCH
        for idx, out in enumerate(outputs):
            it = out.item()
            result.append({class_name.get(idx): it * 100})

        # FOR TF
        # import numpy
        # outputs = outputs.numpy().flatten()
        # _class = 0
        # conf = 0.0
        # for i in range(4):
        #     _class = i
        #     conf = outputs[i]
        #     result.append({class_name.get(_class): conf * 100})
        response = make_response(json.dumps(result))
        return response
    else:
        # save invalid image for later inspection
        time_now = datetime.now().strftime("%Y%m%d_%H%M%S")
        dir_path = os.path.join(str(0), time_now + ".jpg")
        if os.path.exists(os.path.join(cwd, dir_path)):
            time.sleep(1)
            time_now = datetime.now().strftime("%Y%m%d_%H%M%S")
            dir_path = os.path.join(str(0), time_now + ".jpg")
        image.save(os.path.join(cwd, dir_path))
        return make_response(str(result))


@app.route("/getpercent", methods=["POST"])
def predict_percent():
    file = request.files["file"]
    byte_file = file.read()
    outputs = classifier.predict_percent(byte_file)
    result = []
    # FOR PYTORCH
    for idx, out in enumerate(outputs):
        it = out.item()
        result.append({class_name.get(idx): it * 100})

    # FOR TF
    # import numpy
    # outputs = outputs.numpy().flatten()
    # _class = 0
    # conf = 0.0
    # for i in range(4):
    #     _class = i
    #     conf = outputs[i]
    #     result.append({class_name.get(_class): conf * 100})
    response = make_response(json.dumps(result))
    return response


@app.route("/save", methods=["POST"])
def save():
    file = request.files["file"]
    # print(type(file))
    class_id = request.form.get("class")
    time_now = datetime.now().strftime("%Y%m%d_%H%M%S")
    dir_path = os.path.join(str(class_id), time_now + ".jpg")
    if os.path.exists(os.path.join(cwd, dir_path)):
        time.sleep(1)
        time_now = datetime.now().strftime("%Y%m%d_%H%M%S")
        dir_path = os.path.join(str(class_id), time_now + ".jpg")
    file.save(os.path.join(cwd, dir_path))
    return render_template(
        "index.html",
        saved_message="Saved successfully",
        user_image=os.path.join(cwd, dir_path),
    )


@app.route("/submit", methods=["POST"])
def visual_predict_percent():
    file = request.files["file"]
    byte_file = file.read()
    with open(cwd + "/images/" + secure_filename(file.filename), "wb") as binary_file:
        binary_file.write(byte_file)
    save_path = os.path.join(
        os.path.join(cwd, "images"), secure_filename(file.filename)
    )
    outputs = classifier.predict_percent(byte_file)
    result = []
    # FOR PYTORCH
    for idx, out in enumerate(outputs):
        it = out.item()
        result.append({class_name.get(idx): it * 100})

    # FOR TF
    # import numpy
    # outputs = outputs.numpy().flatten()
    # _class = 0
    # conf = 0.0
    # for i in range(4):
    #     _class = i
    #     conf = outputs[i]
    #     result.append({class_name.get(_class): conf * 100})
    return render_template(
        "index.html", message=listToString(result), user_image=save_path
    )


# app.run(port=5000)

import os
import time
from datetime import datetime

import flask
import json
from flask import request
from flask.helpers import make_response

import PredictionPytorch

app = flask.Flask(__name__)
# app.config["DEBUG"] = True

cwd = os.getcwd()
cwd = os.path.join(cwd, "Data_Collector_API")

classifier = PredictionPytorch.ModelPredict(model_path=os.path.join(os.path.join(cwd, 'models'), 'model.pth'))

class_name = {0:'BrownSpot', 1:'Healthy', 2:'Hispa', 3:'LeafBlast'}

@app.route("/predict", methods=["POST"])
def predict():
    file = request.files["image"]
    byte_file = file.read()
    output = classifier.predict(byte_file)
    response = make_response(class_name.get(output))
    return response


@app.route("/getpercent", methods=["POST"])
def predict_percent():
    file = request.files["image"]
    byte_file = file.read()
    outputs = classifier.predict_percent(byte_file)
    result = []
    for idx, out in enumerate(outputs):
        it = out.item()
        result.append({class_name.get(idx):it*100})
    response = make_response(json.dumps(result))
    return response


@app.route("/save", methods=["POST"])
def save():
    file = request.files["image"]
    print(type(file))
    class_id = request.form.get("class")
    time_now = datetime.now().strftime("%Y%m%d_%H%M%S")
    dir_path = os.path.join(str(class_id), time_now + ".jpg")
    if os.path.exists(os.path.join(cwd, dir_path)):
        time.sleep(1)
        time_now = datetime.now().strftime("%Y%m%d_%H%M%S")
        dir_path = os.path.join(str(class_id), time_now + ".jpg")
    file.save(os.path.join(cwd, dir_path))
    response = make_response("TRUE")
    response.content_type = "text/plain; charset=UTF-8"
    return response


app.run()

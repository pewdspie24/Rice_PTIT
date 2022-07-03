import flask
from flask import request
from flask.helpers import make_response
import os
import time

from datetime import datetime

app = flask.Flask(__name__)
# app.config["DEBUG"] = True


@app.route('/predict', methods=['POST'])
def predict():
    file = request.files['image']
    class_id = request.form.get('class')
    time_now = datetime.now().strftime('%Y%m%d_%H%M%S')    
    if os.path.exists(str(class_id) + '/' + time_now + '.jpg'):
        time.sleep(1)
        time_now = datetime.now().strftime('%Y%m%d_%H%M%S') 
    file.save(str(class_id) + '/' + time_now + '.jpg')
    response = make_response("TRUE")
    response.content_type = "text/plain; charset=UTF-8"
    return response


@app.route('/save', methods=['POST'])
def save():
    file = request.files['image']
    class_id = request.form.get('class')
    time_now = datetime.now().strftime('%Y%m%d_%H%M%S')    
    if os.path.exists(str(class_id) + '/' + time_now + '.jpg'):
        time.sleep(1)
        time_now = datetime.now().strftime('%Y%m%d_%H%M%S') 
    file.save(str(class_id) + '/' + time_now + '.jpg')
    response = make_response("TRUE")
    response.content_type = "text/plain; charset=UTF-8"
    return response
app.run()
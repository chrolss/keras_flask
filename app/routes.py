from app import app
from flask import request, redirect, render_template, jsonify
import tensorflow as tf
import os
import argparse
import json
import cv2
from utils.utils import get_yolo_boxes, makedirs
from utils.bbox import draw_boxes
from keras.models import load_model
from tqdm import tqdm
import numpy as np


app.config['UPLOAD_FOLDER'] = 'C:\\Users\\colsson\\uploads'


def load():
    global model
    model = load_model('raccoon.h5')
    global graph
    graph = tf.get_default_graph()


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/upload-image', methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        if 'image' not in request.files:
            print('No image part')
            return redirect(request.url)
        if request.files:
            print("inside requests.files")
            image = request.files['image']
            print("trying to save")
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
            print("image saved")

            return redirect(request.url)

    return render_template("public/upload_image.html")

@app.route('/predict', methods=["GET", "POST"])
def predict():
    #load()
    model = load_model('raccoon.h5')
    graph = tf.get_default_graph()
    with graph.as_default():
        # Setup basic parameters
        net_h, net_w = 416, 416  # a multiple of 32, the smaller the faster
        obj_thresh, nms_thresh = 0.5, 0.45

        # For testing
        image_path = 'C:\\Users\\colsson\\uploads\\raccoon-118.jpg'
        output_path = 'C:\\Users\\colsson\\uploads\\predictions'

        image = cv2.imread(image_path)
        print(image_path)

        # predict the bounding boxes
        boxes = \
            get_yolo_boxes(model, [image], net_h, net_w, config['model']['anchors'], obj_thresh, nms_thresh)[0]

        # draw bounding boxes on the image using labels
        draw_boxes(image, boxes, config['model']['labels'], obj_thresh)

        # write the image with bounding boxes to file
        cv2.imwrite(output_path + image_path.split('/')[-1], np.uint8(image))

    return render_template("public/upload_image.html")


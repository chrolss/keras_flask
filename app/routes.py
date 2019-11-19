from app import app
from flask import request, redirect, render_template, jsonify, url_for, session
import os
import inference

app.config['UPLOAD_FOLDER'] = 'C:\\Users\\colsson\\uploads'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
inference_model = inference.Model()


@app.route('/')
@app.route('/index')
def index():
    return render_template("public/index.html")


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
            session['img_url'] = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            #return redirect(request.url)
            return redirect(url_for('predict_file'))

    return render_template("public/upload_image.html")


@app.route('/predict', methods=["GET", "POST"])
def predict():
    print("Start predicting")
    prediction = inference_model.predict()
    print("Done predicting")

    return jsonify(prediction)


@app.route('/predict_file', methods=["GET", "POST"])
def predict_file():
    print("Start predicting path")
    print(session['img_url'])
    prediction = inference_model.predict_file(session['img_url'])
    print("Done predicting path")
    session['result_img'] = prediction

    return redirect(url_for('display_image'))
    #return jsonify(prediction)


@app.route('/display_image', methods=["GET", "POST"])
def display_image():
    filename = session['result_img']
    print("filename in display_image: " + filename)
    return render_template("display-image.html", img_filepath=filename)


from flask import Flask, jsonify, request
import inference

app = Flask(__name__)
inference_model = inference.Model()

# request model prediction
@app.route('/')
@app.route('/index')
def index():
    return "Hello, world!"


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    print("Start predicting")
    prediction = inference_model.predict()
    print("Done predicting")

    return jsonify(prediction)


# start Flask server
app.run(port=5000, debug=False, threaded=False)


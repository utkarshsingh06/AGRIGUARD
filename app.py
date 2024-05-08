import os

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import keras.utils as Image
import numpy as np
import tensorflow as tf
from keras.applications.resnet import decode_predictions, preprocess_input

app = Flask(__name__)


interpreter = tf.lite.Interpreter(model_path="model/tf2_lite_model.tflite")
interpreter.allocate_tensors()

disease_classes = ['Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy', 'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 'Cherry_(including_sour)___healthy', 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___Common_rust_', 'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 'Grape___Black_rot', 'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy', 'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot', 'Peach___healthy', 'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy', 'Raspberry___healthy', 'Soybean___healthy', 'Squash___Powdery_mildew', 'Strawberry___Leaf_scorch', 'Strawberry___healthy', 'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite', 'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus', 'Tomato___healthy']

def predict(image):

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    interpreter.set_tensor(input_details[0]['index'],image)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])

    predicted_class_index = np.argmax(output_data)
    predicted_class = disease_classes[predicted_class_index]
    return predicted_class

@ app.route('/')
def home():
    return render_template('index.html')
@app.route('/disease')
def disease():
    return render_template('disease.html')

# Define route for prediction
@app.route('/predict', methods=['POST'])
def make_prediction():
    # Get uploaded image file
    if request.method == "POST":
        file = request.files["image"]
        if file:
            filename = secure_filename(file.filename)
            file.save(filename)
            img = Image.load_img(filename, target_size=(256, 256))
            x = Image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = preprocess_input(x)
            predicted_class = predict(x)
            return render_template('result.html', prediction=predicted_class)
    return "Error"
    

if __name__ == '__main__':
    app.run(debug=True)

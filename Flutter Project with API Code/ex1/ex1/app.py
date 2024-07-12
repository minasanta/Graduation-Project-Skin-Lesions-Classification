from flask import Flask,request
import tensorflow as tf
import base64
import cv2
import numpy as np
import tensorflow as tf
from PIL import Image
from keras import Model
from keras.layers import (
    Dense,
    Flatten,
    Activation,
    Dropout,
)
def model_loading():
    irv2 = tf.keras.applications.InceptionResNetV2(
        include_top=True,
        weights="imagenet",
        input_tensor=None,
        input_shape=None,
        pooling=None,
        classifier_activation="softmax",
    )

    conv = irv2.layers[-28].output
    conv = Activation("relu")(conv)
    conv = Dropout(0.5)(conv)
    output = Flatten()(conv)

    output = Dense(512, activation="relu")(output)
    output = Dense(7, activation="softmax")(output)
    model = Model(inputs=irv2.input, outputs=output)

    model.load_weights("F:/ex1/ex1/HAM1000+AUG+IRV2+V2.hdf5")
    return model


MODEL =model_loading()
CLASS_NAMES =  ["Actinic keratoses", "Basal cell carcinoma", "Benign keratosis", "Dermato fibroma", "Melanoma", "Benign nevi", "Vascular lesions"]

app = Flask(__name__)



@app.route('/api',methods = ['Put'] )
def index():
       inputchar = request.get_data()
       imgdata = base64.b64decode(inputchar)
       filename = 'image.jpg'  
       with open(filename, 'wb') as f:
        f.write(imgdata)

        img = cv2.imread('F:/ex1/ex1/image.jpg')
        image = Image.fromarray(img)
        image = image.resize((299, 299))

        img_batch = np.expand_dims(image, 0)
        
        predictions = MODEL.predict(img_batch)
        class_label = np.argmax(predictions)
        predicted_class = CLASS_NAMES[class_label]

        return predicted_class
            

if __name__ == "_main_":
    app.run(debug=True)
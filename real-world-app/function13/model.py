import tensorflow as tf
import numpy as np
import json
import requests

SIZE=128
MODEL_URI='http://159.75.236.13:8501/v1/models/pets:predict'
# MODEL_URI='http://localhost:8501/v1/models/pets:predict'
CLASSES = ['Cat', 'Dog']

def get_prediction(image_path):
    image = tf.keras.preprocessing.image.load_img(image_path, target_size=(SIZE, SIZE))
    image = tf.keras.preprocessing.image.img_to_array(image)
    image = tf.keras.applications.mobilenet_v2.preprocess_input(image)
    image = np.expand_dims(image, axis=0)

    data = json.dumps({
        'instances': image.tolist()
    })
    print(data.encode('utf-8'))
    response = requests.post(MODEL_URI, data=data.encode('utf-8'))
    result = json.loads(response.text)
    print(result)
    prediction = np.squeeze(result['predictions'][0])
    print(prediction)
    class_name = CLASSES[int(prediction > 0.5)]
    return class_name

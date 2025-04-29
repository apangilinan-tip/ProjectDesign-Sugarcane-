
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
import os


class MachineLearning:
    def setup(self):

        # Load the trained model (.h5 file)
        model_path = "weights/inception.h5" 
        self.model = tf.keras.models.load_model(model_path)

    def predict(self, image_path):

        # Load and preprocess the image
        img = image.load_img(image_path, target_size=(128, 128))
        img_array = image.img_to_array(img)  # Convert image to array
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
        img_array /= 255.0  # Normalize pixel values

        # Make a prediction
        
        predictions = self.model.predict(img_array)
        predicted_class = np.argmax(predictions, axis=1)[0]  # Get class with highest probability
        return predicted_class

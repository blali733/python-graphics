from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import argparse
import imutils
import os
from pimutils import resizer

# TESTME check if this code works
# TODO Check if images shouldn't be converted into 0.0-1.0 floats
# TODO think of way of passing used classifier max resolution.
# TODO implement way of passing used classifier max resolution.


class TestClassification:
    def __init__(self, model_name):
        self.model_name = model_name
        if not os.path.isdir("./data/classifiers/" + model_name):
            raise NotADirectoryError()
        self.flair_model = load_model("./data/classifiers/" + model_name + "/models/flair.mod")
        self.t1_model = load_model("./data/classifiers/" + model_name + "/models/t1.mod")
        self.t1c_model = load_model("./data/classifiers/" + model_name + "/models/t1c.mod")
        self.t2_model = load_model("./data/classifiers/" + model_name + "/models/t2.mod")

    def analyze_flair(self, image_part):
        image = resizer.resize(image_part, 28)
        image = np.expand_dims(image, axis=0)
        (tumor, not_tumor) = self.flair_model.predict(image)[0]
        return tumor, not_tumor

    def analyze_t1(self, image_part):
        image = resizer.resize(image_part, 28)
        image = np.expand_dims(image, axis=0)
        (tumor, not_tumor) = self.t1_model.predict(image)[0]
        return tumor, not_tumor

    def analyze_t1c(self, image_part):
        image = resizer.resize(image_part, 28)
        image = np.expand_dims(image, axis=0)
        (tumor, not_tumor) = self.t1c_model.predict(image)[0]
        return tumor, not_tumor

    def analyze_t2(self, image_part):
        image = resizer.resize(image_part, 28)
        image = np.expand_dims(image, axis=0)
        (tumor, not_tumor) = self.t2_model.predict(image)[0]
        return tumor, not_tumor
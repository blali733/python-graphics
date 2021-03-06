from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import os
from src.tools.matrix import resizer
import json


class TestClassification:
    """
    Class containing classification logic.
    """
    def __init__(self, model_name):
        """
        Initializer of classification class, responsible for loading saved model.

        Parameters
        ----------
        model_name : string
            Name of model which should be loaded.
        """
        self.model_name = model_name
        if not os.path.isdir("./data/classifiers/" + model_name):
            raise NotADirectoryError()
        try:
            self.flair_model = load_model("./data/classifiers/" + model_name + "/models/flair.mod")
            self.t1_model = load_model("./data/classifiers/" + model_name + "/models/t1.mod")
            self.t1c_model = load_model("./data/classifiers/" + model_name + "/models/t1c.mod")
            self.t2_model = load_model("./data/classifiers/" + model_name + "/models/t2.mod")
        except ValueError:
            raise FileNotFoundError
        try:
            self.settings = json.load(open("./data/classifiers/"+model_name+"/models/settings.json", "r"))
        except OSError:
            raise FileNotFoundError
        self.maximum = np.iinfo(np.int16).max

    def analyze_flair(self, image_part):
        """
        Method classifying stains according to FLAIR rule-set.

        Parameters
        ----------
        image_part : np.array
            Image part (stain) to be classified.

        Returns
        -------
        float
            Percentage of chances to be tumor.
        float
            Percentage of chances to not be tumor.
        """
        image = resizer.resize(image_part, self.settings.get("size"))
        image = image.astype(np.float) / self.maximum
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)
        (tumor, not_tumor) = self.flair_model.predict(image)[0]
        return tumor, not_tumor

    def analyze_t1(self, image_part):
        """
        Method classifying stains according to T1 rule-set.

        Parameters
        ----------
        image_part : np.array
            Image part (stain) to be classified.

        Returns
        -------
        float
            Percentage of chances to be tumor.
        float
            Percentage of chances to not be tumor.
        """
        image = resizer.resize(image_part, self.settings.get("size"))
        image = image.astype(np.float) / self.maximum
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)
        (tumor, not_tumor) = self.t1_model.predict(image)[0]
        return tumor, not_tumor

    def analyze_t1c(self, image_part):
        """
        Method classifying stains according to T1C rule-set.

        Parameters
        ----------
        image_part : np.array
            Image part (stain) to be classified.

        Returns
        -------
        float
            Percentage of chances to be tumor.
        float
            Percentage of chances to not be tumor.
        """
        image = resizer.resize(image_part, self.settings.get("size"))
        image = image.astype(np.float) / self.maximum
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)
        (tumor, not_tumor) = self.t1c_model.predict(image)[0]
        return tumor, not_tumor

    def analyze_t2(self, image_part):
        """
        Method classifying stains according to T2 rule-set.

        Parameters
        ----------
        image_part : np.array
            Image part (stain) to be classified.

        Returns
        -------
        float
            Percentage of chances to be tumor.
        float
            Percentage of chances to not be tumor.
        """
        image = resizer.resize(image_part, self.settings.get("size"))
        image = image.astype(np.float) / self.maximum
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)
        (tumor, not_tumor) = self.t2_model.predict(image)[0]
        return tumor, not_tumor

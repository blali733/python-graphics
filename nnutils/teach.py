# set the matplotlib backend so figures can be saved in the background
import matplotlib
matplotlib.use("Agg")
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from keras.preprocessing.image import img_to_array
from keras.utils import to_categorical
import matplotlib.pyplot as plt
import numpy as np
import random
import os
from pimutils import resizer
from osutils import inlineprogress as pbar, adfIO, pathtools


class Teacher:
    def __init__(self, epochs=25, initial_learning_rate=1e-3, batch_size=25, model_frame_size=28):
        self.epochs = epochs
        self.initial_learning_rate = initial_learning_rate
        self.batch_size = batch_size
        if model_frame_size == 28:
            from nnutils.models import c28x28
            self.model_cooker = c28x28.Net28px()
            self.image_size = 28
        else:
            from nnutils.models import c28x28
            self.model_cooker = c28x28.Net28px()
            self.image_size = 28

    def teach(self, model_name, random_seed=666):
        random.seed(random_seed)
        print("STEP 1: Loading images:")
        data_flair = []
        labels_flair = []
        data_t1 = []
        labels_t1 = []
        data_t1c = []
        labels_t1c = []
        data_t2 = []
        labels_t2 = []
        print("STEP 1a: flair:")
        for root, subFolders, files in os.walk("./data/parsed/flair"):
            files_count = len(files)
            done_count = 0
            random.shuffle(files)
            for file in files:
                image = adfIO.load(os.path.join(root, file))
                if image != -1:
                    data_flair.append(resizer.resize(image, self.image_size))
                    label = pathtools.get_folder_name_from_path(os.path.join(root, file), -2)
                    label = 1 if label == "tumor" else 0
                    labels_flair.append(label)
                done_count += 1
                pbar.inline_out_of_progress(done_count, files_count, "files")


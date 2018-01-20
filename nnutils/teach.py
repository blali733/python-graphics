# set the matplotlib backend so figures can be saved in the background
import pathlib

import matplotlib
import shutil

matplotlib.use("Agg")
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
import matplotlib.pyplot as plt
import numpy as np
import random
import os
from pimutils import resizer
from osutils import inlineprogress as pbar, adfIO, pathtools

# TESTME check if this code works
# TODO Implement storeing classifier parameters into JSON file.
# TODO Check if images shouldn't be converted into 0.0-1.0 floats


def prepare_dirs(model_name):
    shutil.rmtree('./data/classifiers/' + model_name, ignore_errors=True)
    pathlib.Path('./data/classifiers/' + model_name).mkdir(parents=True, exist_ok=True)
    pathlib.Path('./data/classifiers/' + model_name + '/models').mkdir(parents=True, exist_ok=True)
    pathlib.Path('./data/classifiers/' + model_name + '/plots').mkdir(parents=True, exist_ok=True)


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

    def teach(self, model_name, random_seed=666, test_size=0.25):
        random.seed(random_seed)
        prepare_dirs(model_name)
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
        print("STEP 1b: t1:")
        for root, subFolders, files in os.walk("./data/parsed/t1"):
            files_count = len(files)
            done_count = 0
            random.shuffle(files)
            for file in files:
                image = adfIO.load(os.path.join(root, file))
                if image != -1:
                    data_t1.append(resizer.resize(image, self.image_size))
                    label = pathtools.get_folder_name_from_path(os.path.join(root, file), -2)
                    label = 1 if label == "tumor" else 0
                    labels_t1.append(label)
                done_count += 1
                pbar.inline_out_of_progress(done_count, files_count, "files")
        print("STEP 1c: t1c:")
        for root, subFolders, files in os.walk("./data/parsed/t1c"):
            files_count = len(files)
            done_count = 0
            random.shuffle(files)
            for file in files:
                image = adfIO.load(os.path.join(root, file))
                if image != -1:
                    data_t1c.append(resizer.resize(image, self.image_size))
                    label = pathtools.get_folder_name_from_path(os.path.join(root, file), -2)
                    label = 1 if label == "tumor" else 0
                    labels_t1c.append(label)
                done_count += 1
                pbar.inline_out_of_progress(done_count, files_count, "t2")
        print("STEP 1d: t2:")
        for root, subFolders, files in os.walk("./data/parsed/flair"):
            files_count = len(files)
            done_count = 0
            random.shuffle(files)
            for file in files:
                image = adfIO.load(os.path.join(root, file))
                if image != -1:
                    data_t2.append(resizer.resize(image, self.image_size))
                    label = pathtools.get_folder_name_from_path(os.path.join(root, file), -2)
                    label = 1 if label == "tumor" else 0
                    labels_t2.append(label)
                done_count += 1
                pbar.inline_out_of_progress(done_count, files_count, "files")
        print("STEP 2: Splitting data:")
        print("STEP 2a: flair")
        (train_x_flair, test_x_flair, train_y_flair, test_y_flair) = train_test_split(data_flair, labels_flair,
                                                                                      test_size=test_size,
                                                                                      random_state=random_seed)
        train_y_flair = to_categorical(train_y_flair, num_classes=2)
        test_y_flair = to_categorical(test_y_flair, num_classes=2)
        print("STEP 2b: t1")
        (train_x_t1, test_x_t1, train_y_t1, test_y_t1) = train_test_split(data_t1, labels_t1,
                                                                          test_size=test_size,
                                                                          random_state=random_seed)
        train_y_t1 = to_categorical(train_y_t1, num_classes=2)
        test_y_t1 = to_categorical(test_y_t1, num_classes=2)
        print("STEP 2c: t1c")
        (train_x_t1c, test_x_t1c, train_y_t1c, test_y_t1c) = train_test_split(data_t1c, labels_t1c,
                                                                              test_size=test_size,
                                                                              random_state=random_seed)
        train_y_t1c = to_categorical(train_y_t1c, num_classes=2)
        test_y_t1c = to_categorical(test_y_t1c, num_classes=2)
        print("STEP 2d: t2")
        (train_x_t2, test_x_t2, train_y_t2, test_y_t2) = train_test_split(data_t2, labels_t2,
                                                                          test_size=test_size,
                                                                          random_state=random_seed)
        train_y_t2 = to_categorical(train_y_t2, num_classes=2)
        test_y_t2 = to_categorical(test_y_t2, num_classes=2)
        print("STEP 3: creating augmentation settings")
        aug = ImageDataGenerator(rotation_range=30, width_shift_range=0.1,
                                 height_shift_range=0.1, shear_range=0.2, zoom_range=0.2,
                                 horizontal_flip=True, fill_mode="nearest")
        values = [(train_x_flair, test_x_flair, train_y_flair, test_y_flair),
                  (train_x_t1, test_x_t1, train_y_t1, test_y_t1),
                  (train_x_t1c, test_x_t1c, train_y_t1c, test_y_t1c),
                  (train_x_t2, test_x_t2, train_y_t2, test_y_t2)]
        for i in range(4):
            trainX = values[i][0]
            testX = values[i][1]
            trainY = values[i][2]
            testY = values[i][3]
            if i == 0:
                print("Flair model:")
                name = "flair"
            elif i == 1:
                print("T1 model:")
                name ="t1"
            elif i == 2:
                print("T1c model:")
                name = "t1c"
            else:
                print("T2 model:")
                name = "t2"
            print("STEP 4: Compiling model")
            model = self.model_cooker.build(width=self.image_size, height=self.image_size, depth=1, classes=2)
            opt = Adam(lr=self.initial_learning_rate, decay=self.initial_learning_rate/self.epochs)
            model.compile(loss="binary_crossentropy", optimizer=opt, metrics=["accuracy"])
            print("STEP 5: Training network")
            H = model.fit_generator(aug.flow(trainX, trainY, batch_size=self.batch_size),
                                    validation_data=(testX, testY), steps_per_epoch=len(trainX) // self.batch_size,
                                    epochs=self.epochs, verbose=1)
            print("STEP 6: Saving network")
            model.save("./data/classifiers/"+model_name+"/models/"+name+".mod")
            print("STEP 7: Plotting training loss and accuracy")
            # plot the training loss and accuracy
            plt.style.use("ggplot")
            plt.figure()
            N = self.epochs
            plt.plot(np.arange(0, N), H.history["loss"], label="train_loss")
            plt.plot(np.arange(0, N), H.history["val_loss"], label="val_loss")
            plt.plot(np.arange(0, N), H.history["acc"], label="train_acc")
            plt.plot(np.arange(0, N), H.history["val_acc"], label="val_acc")
            plt.title("Training Loss and Accuracy on tumor/not tumor for "+name+" images.")
            plt.xlabel("Epoch #")
            plt.ylabel("Loss/Accuracy")
            plt.legend(loc="lower left")
            plt.savefig("./data/classifiers/"+model_name+"/plots/"+name+".png")


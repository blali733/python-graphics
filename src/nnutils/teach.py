from keras.preprocessing.image import ImageDataGenerator, img_to_array
from keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
import matplotlib.pyplot as plt
import numpy as np
import random
import os
from src.osutils import pathtools
from src.osutils.fileIO.directories import prepare_dirs
from src.tools.matrix import resizer
from src.osutils import inlineprogress as pbar
from src.osutils.fileIO import adfIO
import json


class Teacher:
    """
    Class containing logic connected to training classifier.
    """
    def __init__(self, epochs=25, initial_learning_rate=1e-3, batch_size=25, model_name="LENET"):
        """
        Initializer of classifier teaching class.

        Parameters
        ----------
        epochs : int
            Number of epochs.
        initial_learning_rate : float
            Starting learning rate of neural network.
        batch_size : int
            Number of single images processed at once.
        model_frame_size : int
            Defines dimensions of single input image (automatically rescaled).
        model_name: string
            Defines model used as classifier.
        """
        print(model_name)
        self.epochs = epochs
        self.initial_learning_rate = initial_learning_rate
        self.batch_size = batch_size
        if model_name == "VGG":
            from src.nnutils.models import VGGNet
            self.model_cooker = VGGNet.VGGNet()
            self.image_size = 224
        elif model_name == "SIMPLEVGG":
            from src.nnutils.models import SmallerVGGNet
            self.model_cooker = SmallerVGGNet.SmallerVGGNet()
            self.image_size = 96
        else:   # Defaults to LeNet:
            from src.nnutils.models import LeNet
            self.model_cooker = LeNet.LeNet()
            self.image_size = 28
        self.settings = {"version": 1, "size": self.image_size, "classifier_name": model_name}

    def teach(self, model_name, random_seed=666, test_size=0.25):
        """
        Method containing full procedure train to teach new classifier.

        Parameters
        ----------
        model_name : string
            Name of created model.
        random_seed : int
            Seed for pseudo random number generator to ensure repeatability.
        test_size : float
            Percent (0.0 - 1.0) of data used as testing set.
        """
        print(self.model_cooker.name())
        random.seed(random_seed)
        prepare_dirs(model_name)
        print("STEP 1: Loading images:")
        data_flair = []
        labels_flair = []
        # data_t1 = []
        # labels_t1 = []
        # data_t1c = []
        # labels_t1c = []
        # data_t2 = []
        # labels_t2 = []
        print("STEP 1a: flair:")
        for root, subFolders, files in os.walk("./data/parsed/flair"):
            files_count = len(files)
            done_count = 0
            random.shuffle(files)
            for file in files:
                try:
                    image = adfIO.load(os.path.join(root, file), True)
                    img_res = resizer.resize(image, self.image_size)
                    img = img_to_array(img_res)
                    if img.shape[0] != img.shape[1]:
                        print("err")
                    data_flair.append(img)
                    label = pathtools.get_folder_name_from_path(os.path.join(root, file), -2)
                    label = 1 if label == "tumor" else 0
                    labels_flair.append(label)
                except FileExistsError:
                    print("Corrupted file")
                done_count += 1
                pbar.inline_out_of_progress(done_count, files_count, "files")
        # print("STEP 1b: t1:")
        # for root, subFolders, files in os.walk("./data/parsed/t1"):
        #     files_count = len(files)
        #     done_count = 0
        #     random.shuffle(files)
        #     for file in files:
        #         try:
        #             image = adfIO.load(os.path.join(root, file), True)
        #             data_t1.append(img_to_array(resizer.resize(image, self.image_size)))
        #             label = pathtools.get_folder_name_from_path(os.path.join(root, file), -2)
        #             label = 1 if label == "tumor" else 0
        #             labels_t1.append(label)
        #         except FileExistsError:
        #             print("Corrupted file")
        #         done_count += 1
        #         pbar.inline_out_of_progress(done_count, files_count, "files")
        # print("STEP 1c: t1c:")
        # for root, subFolders, files in os.walk("./data/parsed/t1c"):
        #     files_count = len(files)
        #     done_count = 0
        #     random.shuffle(files)
        #     for file in files:
        #         try:
        #             image = adfIO.load(os.path.join(root, file), True)
        #             data_t1c.append(img_to_array(resizer.resize(image, self.image_size)))
        #             label = pathtools.get_folder_name_from_path(os.path.join(root, file), -2)
        #             label = 1 if label == "tumor" else 0
        #             labels_t1c.append(label)
        #         except FileExistsError:
        #             print("Corrupted file")
        #         done_count += 1
        #         pbar.inline_out_of_progress(done_count, files_count, "files")
        # print("STEP 1d: t2:")
        # for root, subFolders, files in os.walk("./data/parsed/t2"):
        #     files_count = len(files)
        #     done_count = 0
        #     random.shuffle(files)
        #     for file in files:
        #         try:
        #             image = adfIO.load(os.path.join(root, file), True)
        #             data_t2.append(img_to_array(resizer.resize(image, self.image_size)))
        #             label = pathtools.get_folder_name_from_path(os.path.join(root, file), -2)
        #             label = 1 if label == "tumor" else 0
        #             labels_t2.append(label)
        #         except FileExistsError:
        #             print("Corrupted file")
        #         done_count += 1
        #         pbar.inline_out_of_progress(done_count, files_count, "files")
        print("STEP 2: Splitting data:")
        maximum = np.iinfo(np.int16).max
        print("STEP 2a: flair")
        data_flair_arr = np.array(data_flair, dtype=np.float) / maximum
        labels_flair_arr = np.array(labels_flair)
        (train_x_flair, test_x_flair, train_y_flair, test_y_flair) = train_test_split(data_flair_arr, labels_flair_arr,
                                                                                      test_size=test_size,
                                                                                      random_state=random_seed)
        train_y_flair = to_categorical(train_y_flair, num_classes=2)
        test_y_flair = to_categorical(test_y_flair, num_classes=2)
        # print("STEP 2b: t1")
        # data_t1 = np.array(data_t1, dtype=np.float) / maximum
        # labels_t1 = np.array(labels_t1)
        # (train_x_t1, test_x_t1, train_y_t1, test_y_t1) = train_test_split(data_t1, labels_t1,
        #                                                                   test_size=test_size,
        #                                                                   random_state=random_seed)
        # train_y_t1 = to_categorical(train_y_t1, num_classes=2)
        # test_y_t1 = to_categorical(test_y_t1, num_classes=2)
        # print("STEP 2c: t1c")
        # data_t1c = np.array(data_t1c, dtype=np.float) / maximum
        # labels_t1c = np.array(labels_t1c)
        # (train_x_t1c, test_x_t1c, train_y_t1c, test_y_t1c) = train_test_split(data_t1c, labels_t1c,
        #                                                                       test_size=test_size,
        #                                                                       random_state=random_seed)
        # train_y_t1c = to_categorical(train_y_t1c, num_classes=2)
        # test_y_t1c = to_categorical(test_y_t1c, num_classes=2)
        # print("STEP 2d: t2")
        # data_t2 = np.array(data_t2, dtype=np.float) / maximum
        # labels_t2 = np.array(labels_t2)
        # (train_x_t2, test_x_t2, train_y_t2, test_y_t2) = train_test_split(data_t2, labels_t2,
        #                                                                   test_size=test_size,
        #                                                                   random_state=random_seed)
        # train_y_t2 = to_categorical(train_y_t2, num_classes=2)
        # test_y_t2 = to_categorical(test_y_t2, num_classes=2)
        print("STEP 3: creating augmentation settings")
        aug = ImageDataGenerator(rotation_range=30, width_shift_range=0.1,
                                 height_shift_range=0.1, shear_range=0.2, zoom_range=0.2,
                                 horizontal_flip=True, fill_mode="nearest")
        values = [(train_x_flair, test_x_flair, train_y_flair, test_y_flair)] # ,
                  # (train_x_t1, test_x_t1, train_y_t1, test_y_t1),
                  # (train_x_t1c, test_x_t1c, train_y_t1c, test_y_t1c),
                  # (train_x_t2, test_x_t2, train_y_t2, test_y_t2)]
        for i in range(1):
            trainX = values[i][0]
            testX = values[i][1]
            trainY = values[i][2]
            testY = values[i][3]
            if i == 0:
                print("Flair model:")
                name = "flair"
            # elif i == 1:
            #     print("T1 model:")
            #     name ="t1"
            # elif i == 2:
            #     print("T1c model:")
            #     name = "t1c"
            # else:
            #     print("T2 model:")
            #     name = "t2"
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
        json.dump(self.settings, open("./data/classifiers/"+model_name+"/models/settings.json", "w"))

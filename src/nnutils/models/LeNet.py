# Created basing on https://www.pyimagesearch.com/2017/12/11/image-classification-with-keras-and-deep-learning/
from keras.models import Sequential
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.layers.core import Activation
from keras.layers.core import Flatten
from keras.layers.core import Dense
from keras import backend


class LeNet:
    """
    Model Name:
        LeNet
        A model based on LeNet network, implemented by Adrian Rosebrock.

    Recommended image size:
        28x28 px
    """

    def name(self):
        """
        Method printing name of used model.
        """
        print("LeNet")

    @staticmethod
    def build(width, height, depth, classes):
        """
        Method which builds convolutional neural network which would serve as classifier model.

        Parameters
        ----------
        width : int
        height : int
        depth : int
        classes : int

        Returns
        -------
        Constructed sequential model of neural network
        """
        # initialize the model
        model = Sequential()
        input_shape = (height, width, depth)

        # if we are using "channels first", update the input shape
        if backend.image_data_format() == "channels_first":
            input_shape = (depth, height, width)

        # first set of CONV => RELU => POOL layers
        model.add(Conv2D(20, (5, 5), padding="same", input_shape=input_shape))
        model.add(Activation("relu"))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

        # second set of CONV => RELU => POOL layers
        model.add(Conv2D(50, (5, 5), padding="same"))
        model.add(Activation("relu"))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

        # first (and only) set of FC => RELU layers
        model.add(Flatten())
        model.add(Dense(500))
        model.add(Activation("relu"))

        # softmax classifier
        model.add(Dense(classes))
        model.add(Activation("softmax"))

        # return the constructed network architecture
        return model

# Created basing on http://dandxy89.github.io/ImageModels/vgg19/
from keras.models import Sequential
from keras.layers.convolutional import Convolution2D
from keras.layers.convolutional import MaxPooling2D
from keras.layers.convolutional import ZeroPadding2D
from keras.layers.core import Activation
from keras.layers.core import Flatten
from keras.layers.core import Dropout
from keras.layers.core import Dense
from keras import backend


class VGGNet:
    """
    Model Name:
        VGG-19
        A model of the 19-layer network used by the VGG team in the ILSVRC-2014 competition.

    Paper:
         Very Deep Convolutional Networks for Large-Scale Image Recognition - K. Simonyan, A. Zisserman
         arXiv:1409.1556

    Recommended image size:
        224x224 px
    """

    def name(self):
        """
        Method printing name of used model.
        """
        print("VGG")

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
        chan_dim = -1

        # if we are using "channels first", update the input shape
        if backend.image_data_format() == "channels_first":
            input_shape = (depth, height, width)
            chan_dim = 1

        # Layer Cluster - 1
        model.add(ZeroPadding2D(padding=(1, 1), input_shape=input_shape))
        model.add(Convolution2D(64, (3, 3), padding='same'))
        model.add(Activation('relu'))
        model.add(ZeroPadding2D(padding=(1, 1)))
        model.add(Convolution2D(64, (3, 3), padding='same'))
        model.add(Activation('relu'))
        model.add(MaxPooling2D((2, 2), strides=(2, 2)))

        # Layer Cluster - 2
        model.add(ZeroPadding2D(padding=(1, 1)))
        model.add(Convolution2D(128, (3, 3), padding='same'))
        model.add(Activation('relu'))
        model.add(ZeroPadding2D(padding=(1, 1)))
        model.add(Convolution2D(128, (3, 3), padding='same'))
        model.add(Activation('relu'))
        model.add(MaxPooling2D((2, 2), strides=(2, 2)))

        # Layer Cluster - 3
        model.add(ZeroPadding2D(padding=(1, 1)))
        model.add(Convolution2D(256, (3, 3), padding='same'))
        model.add(Activation('relu'))
        model.add(ZeroPadding2D(padding=(1, 1)))
        model.add(Convolution2D(256, (3, 3), padding='same'))
        model.add(Activation('relu'))
        model.add(ZeroPadding2D(padding=(1, 1)))
        model.add(Convolution2D(256, (3, 3), padding='same'))
        model.add(Activation('relu'))
        model.add(ZeroPadding2D(padding=(1, 1)))
        model.add(Convolution2D(256, (3, 3), padding='same'))
        model.add(Activation('relu'))
        model.add(MaxPooling2D((2, 2), strides=(2, 2)))

        # Layer Cluster - 4
        model.add(ZeroPadding2D(padding=(1, 1)))
        model.add(Convolution2D(512, (3, 3), padding='same'))
        model.add(Activation('relu'))
        model.add(ZeroPadding2D(padding=(1, 1)))
        model.add(Convolution2D(512, (3, 3), padding='same'))
        model.add(Activation('relu'))
        model.add(ZeroPadding2D(padding=(1, 1)))
        model.add(Convolution2D(512, (3, 3), padding='same'))
        model.add(Activation('relu'))
        model.add(ZeroPadding2D(padding=(1, 1)))
        model.add(Convolution2D(512, (3, 3), padding='same'))
        model.add(Activation('relu'))
        model.add(MaxPooling2D((2, 2), strides=(2, 2)))

        # Layer Cluster - 5 - Output Layer
        model.add(Flatten())
        model.add(Dense(4096))
        model.add(Activation('relu'))
        model.add(Dropout(0.5))
        model.add(Dense(4096))
        model.add(Activation('relu'))
        model.add(Dropout(0.5))
        model.add(Dense(classes))
        model.add(Activation('softmax'))

        # return the constructed network architecture
        return model

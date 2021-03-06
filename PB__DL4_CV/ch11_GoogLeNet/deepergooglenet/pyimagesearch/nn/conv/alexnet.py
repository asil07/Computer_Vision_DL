from keras.models import Sequential
from keras.layers.normalization.batch_normalization import BatchNormalization
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.layers.core import Activation, Flatten, Dense, Dropout
from keras.regularizers import l2
from keras import backend as K


class AlexNet:
    @staticmethod
    def build(width, height, depth, classes, reg=0.0002):
        model = Sequential()
        inputShape = (height, width, depth)
        chanDim = -1

        if K.image_data_format() == "channel_first":
            inputShape = (depth, height, width)
            chanDim = 1

        # >>>>>>>>>>>>>>>>> block 1: CONV => RELU => POOL <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        model.add(Conv2D(96, (11, 11), strides=(4, 4), input_shape=inputShape, padding="same",
                         kernel_regularizer=l2(reg)))
        model.add(Activation(activation="relu"))
        model.add(BatchNormalization(axis=chanDim))
        model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2)))
        model.add(Dropout(0.25))

        # >>>>>>>>>>>>>>>>> block 2: CONV => RELU > POOL <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        model.add(Conv2D(256, (5, 5), padding="same", kernel_regularizer=l2(reg)))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=chanDim))
        model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2)))
        model.add(Dropout(0.25))

        # >>>>>>>>>>>>>>>> block 3: COND > RELU > CONV > RELU > CONV > RELU > POOl <<<<<<<<<<<<<
        model.add(Conv2D(384, (3, 3), padding="same", kernel_regularizer=l2(reg)))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=chanDim))

        model.add(Conv2D(384, (3, 3), padding="same", kernel_regularizer=l2(reg)))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=chanDim))

        model.add(Conv2D(256, (3, 3), padding="same", kernel_regularizer=l2(reg)))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=chanDim))
        model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2)))
        model.add(Dropout(0.25))

        # >>>>>>>>>>>>>>>>> block 4: first set of FC > RELU layers <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        model.add(Flatten())
        model.add(Dense(4096, kernel_regularizer=l2(reg)))
        model.add(Activation("relu"))
        model.add(BatchNormalization())
        model.add(Dropout(0.5))

        # >>>>>>>>>>>>>>>>> block 5: second set of FC > RELU layers <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        model.add(Dense(4096, kernel_regularizer=l2(reg)))
        model.add(Activation("relu"))
        model.add(BatchNormalization())
        model.add(Dropout(0.5))

        # softmax classifier
        model.add(Dense(classes, kernel_regularizer=l2(reg)))
        model.add(Activation('softmax'))

        return model

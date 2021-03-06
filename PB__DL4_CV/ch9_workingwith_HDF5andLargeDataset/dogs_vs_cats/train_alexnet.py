import matplotlib
matplotlib.use("Agg")

from config import dogs_vs_cats_config as config
from pyimagesearch.preprocessing.imagetoarraypreprocessor import ImageToArrayPreprocessor
from pyimagesearch.preprocessing.simplepreprocessor import SimplePreprocessor
from pyimagesearch.preprocessing.patchpreprocessor import PatchPreprocessor
from pyimagesearch.preprocessing.meanpreprocessor import MeanPreprocessor
from pyimagesearch.callbacks.trainingmonitor import TrainingMonitor
from pyimagesearch.io.hdf5datasetgenerator import HDF5DatasetGenerator
from pyimagesearch.nn.conv.alexnet import AlexNet
from keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam, SGD
import json
import os

aug = ImageDataGenerator(rotation_range=20, zoom_range=0.15, width_shift_range=0.2,
                         height_shift_range=0.2, shear_range=0.15, horizontal_flip=True,
                         fill_mode="nearest")
means = json.loads(open(config.DATASET_MEAN).read())

# preprocessors
sp = SimplePreprocessor(227, 227)
pp = PatchPreprocessor(227, 227)
mp = MeanPreprocessor(means["R"], means["G"], means["B"])
iap = ImageToArrayPreprocessor()

# initializes dataset for train and validation
trainGen = HDF5DatasetGenerator(config.TRAIN_HDF5, 128, preprocessors=[pp, mp, iap],
                                aug=aug, classes=2)
valGen = HDF5DatasetGenerator(config.VAL_HDF5, 128, preprocessors=[sp, mp, iap],
                              classes=2)

print("SABR: compiling model . . .")
opt = SGD(learning_rate=0.1)
model = AlexNet.build(width=227, height=227, depth=3, classes=2, reg=0.0002)
model.compile(loss="binary_crossentropy", optimizer=opt, metrics=["accuracy"])

path = os.path.sep.join([config.OUTPUT_PATH, f"{os.getpid()}"])
callbacks = [TrainingMonitor(path)]

# train network
print("SABR: boshlandi . . . ")
model.fit(trainGen.generator(), steps_per_epoch=trainGen.numImages // 128,
          validation_data=valGen.generator(), validation_steps=valGen.numImages // 128,
          epochs=1, max_queue_size=128 * 2, callbacks=callbacks, verbose=1)

print("INFO: serializing model . . .")
model.save(config.MODEL_PATH, overwrite=True)

trainGen.close()
valGen.close()






import matplotlib

matplotlib.use("Agg")
from sklearn.preprocessing import LabelBinarizer
from sklearn.metrics import classification_report
from pyimagesearch.nn.conv.minivggnet import MiniVGGNet
from tensorflow.keras.optimizers import SGD
from keras.datasets import cifar10
import matplotlib.pyplot as plt
import numpy as np
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-o", '--output', required=True)
ap.add_argument("-m", "--model", required=True)
args = vars(ap.parse_args())

print("INFO loading cifar-10 ...")
((trainX, trainY), (testX, testY)) = cifar10.load_data()

trainX = trainX.astype("float") / 255.0
testX = testX.astype("float") / 255.0

lb = LabelBinarizer()
trainY = lb.fit_transform(trainY)
testY = lb.transform(testY)

labelNames = ["airplane", "automobile", "bird", "cat", "deer",
              "dog", "frog", "horse", "ship", "truck"]

print("INFO compiling model ...")
opt = SGD(learning_rate=0.01, decay=0.01 / 2, momentum=0.9, nesterov=True)
model = MiniVGGNet.build(width=32, height=32, depth=3, classes=10)
model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=["accuracy"])

# train
print("INFO training network ...")
H = model.fit(trainX, trainY, validation_data=(testX, testY),
              batch_size=64, epochs=2, verbose=1)
model.save(args["model"])

print("INFO evaluating network ...")
predictions = model.predict(testX, batch_size=64)
print(classification_report(testY.argmax(axis=1), predictions.argmax(axis=1),
                            target_names=labelNames))

# plot the training loss and accuracy
plt.style.use("ggplot")
plt.figure()
plt.plot(np.arange(0, 2), H.history["loss"], label="train_loss")
plt.plot(np.arange(0, 2), H.history["val_loss"], label="val_loss")
plt.plot(np.arange(0, 2), H.history["acc"], label="train_acc")
plt.plot(np.arange(0, 2), H.history["val_acc"], label="val_acc")
plt.title("Training Loss and Accuracy on CIFAR-10")
plt.xlabel("Epoch #")
plt.ylabel("Loss/Accuracy")
plt.legend()
plt.savefig(args["output"])




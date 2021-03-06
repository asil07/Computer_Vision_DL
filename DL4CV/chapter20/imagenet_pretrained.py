from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications import InceptionV3
from tensorflow.keras.applications import Xception
from tensorflow.keras.applications import VGG16
from tensorflow.keras.applications import VGG19
from tensorflow.keras.applications import imagenet_utils
from tensorflow.keras.applications.inception_v3 import preprocess_input
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import load_img
import numpy as np
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True)
ap.add_argument("-model", "--model", type=str, default="vgg16")
args = vars(ap.parse_args())

MODELS = {
    "vgg16": VGG16,
    "vgg19": VGG19,
    "inception": InceptionV3,
    "xception": Xception,
    "resnet": ResNet50
}


if args["model"] not in MODELS.keys():
    raise AssertionError("The -- model command line argument should "
                         "be a key in the 'MODELS' dictionary")

input_shape = (224, 224)
preprocess = imagenet_utils.preprocess_input

if args["model"] in ("inception", "xception"):
    input_shape = (299, 299)
    preprocess = preprocess_input

print(f"INFO loading {args['model']}...")
Network = MODELS[args["model"]]
model = Network(weights="imagenet")

print("INFO: laoding and pre-processing image...")
image = load_img(args["image"], target_size=input_shape)
image = img_to_array(image)
image = np.expand_dims(image, axis=0)
image = preprocess(image)

print(f"INFO: classifying image with {args['model']}")
preds = model.predict(image)
P = imagenet_utils.decode_predictions(preds)

for (i, (imagenetID, label, prob)) in enumerate(P[0]):
    print(f'{i + 1}, {label}, {prob * 100:.2f}%')

orig = cv2.imread(args["image"])

scale_percent = 50
width = int(orig.shape[1] * scale_percent / 100)
height = int(orig.shape[0] * scale_percent / 100)
dim = (width, height)
resized = cv2.resize(orig, dim, interpolation=cv2.INTER_AREA)

(imagenetID, label, prob) = P[0][0]
cv2.putText(resized, f"Label: {label}", (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

cv2.imshow("Classification", resized)
cv2.waitKey(0)













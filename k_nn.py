from imutils import paths
from keras.preprocessing.image import img_to_array
import numpy as np
import cv2
import os
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical



data = []
labels = []

# grab the image paths and randomly shuffle them
imagePaths = sorted(list(paths.list_images("dataset_for_models")))


# loop over the input images
for imagePath in imagePaths:
    # load the image, pre-process it, and store it in the data list
    image = cv2.imread(imagePath)
    print(imagePath)
    image = cv2.resize(image, (48, 48))
    image = img_to_array(image)
    data.append(image)

    # extract the class label from the image path and update the
	# labels list
    label = imagePath.split(os.path.sep)[-2]
    if label == "model":
        label = 1
    else:
        label = 0
    labels.append(label)

data = np.array(data, dtype="float") / 255.0
labels = np.array(labels)
print(data.shape)

trainX, testX, trainY, testY = train_test_split(data, labels, test_size = 0.2, random_state = 42)

# convert the labels from integers to vectors
trainY = to_categorical(trainY, num_classes=2)
testY = to_categorical(testY, num_classes=2)

from sklearn.linear_model import LogisticRegression
from sklearn import metrics

knn = LogisticRegression()
knn.fit(trainX, trainY)

pred = knn.predict(testX)
score = metrics.accuracy_score(testY, pred)
print(score)

cm = metrics.confusion_matrix(testY, pred, labels=['model', 'not_model'])
print(cm)

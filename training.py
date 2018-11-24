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
imagePaths = sorted(list(paths.list_images("dataset")))


# loop over the input images
label_dict ={}
for imagePath in imagePaths:
    # load the image, pre-process it, and store it in the data list
    image = cv2.imread(imagePath)
    print(imagePath)
    image = cv2.resize(image, (48, 48))
    image = img_to_array(image)
    data.append(image)

    # extract the class label from the image path and update the
	# labels list
    list_labels = os.listdir(path="dataset")
    number_labels = len(list_labels)
    label_dir = imagePath.split(os.path.sep)[-2]
    label = list_labels.index(label_dir)
    label_dict[label_dir] = label
    print(label)
    labels.append(label)

# scale the raw pixel intensities to the range [0, 1]
data = np.array(data, dtype="float") / 255.0
labels = np.array(labels)
print(data.shape)
print(labels)
with open('dict_labels', 'w') as file:
    for key, value in label_dict.items():
        file.write(key + ' ' + str(value) + '\n')

trainX, testX, trainY, testY = train_test_split(data, labels, test_size = 0.2, random_state = 42, stratify= labels)
print(trainX[0])
# convert the labels from integers to vectors
trainY = to_categorical(trainY, num_classes=number_labels)
testY = to_categorical(testY, num_classes=number_labels)

from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten, Activation
from keras.layers.convolutional import MaxPooling2D
from keras.preprocessing.image import ImageDataGenerator
model = Sequential()

model.add(Conv2D(50, (5, 5), padding="same", input_shape=(48, 48, 3)))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
model.add(Conv2D(50, (5, 5), padding="same"))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

model.add(Flatten())
model.add(Dense(700))
model.add(Activation("relu"))

# softmax classifier
model.add(Dense(number_labels))
model.add(Activation("softmax"))


model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])

aug = ImageDataGenerator(rotation_range=10, width_shift_range=0.1,
	height_shift_range=0.1, shear_range=0.2, zoom_range=0.2,
	horizontal_flip=True, fill_mode="nearest")

#model.fit(trainX, trainY, epochs=100)
model.fit_generator(aug.flow(trainX, trainY),
	validation_data=(testX, testY), steps_per_epoch=550,
	epochs=10, verbose=1)
score, acc = model.evaluate(testX, testY, batch_size=128)
print(score, acc)
model.save('model_tanks')


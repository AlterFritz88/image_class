from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import cv2

image = cv2.imread("st.jpeg")
image = cv2.resize(image, (48, 48))
image = image.astype("float") / 255.0
image = img_to_array(image)
image = np.expand_dims(image, axis=0)

model = load_model('model_tanks')

labels_dict = {}
with open('dict_labels', 'r') as file:
    for line in file:
        if len(line) > 3:
            items = line[:-1].split(' ')
            labels_dict[int(items[1])] = items[0]

list_of_pred = model.predict(image)[0]
top = sorted(range(len(list_of_pred)), key=lambda i: list_of_pred[i], reverse=True)[:3]
for i in top:
    print(labels_dict[i], list_of_pred[i])
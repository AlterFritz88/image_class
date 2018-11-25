from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from sklearn.pipeline import Pipeline
from transliterate import translit
import pickle
from keras.utils import to_categorical
from sklearn.feature_extraction.text import  TfidfVectorizer


labels = []
data_dict = {}
data = []
label = []
vectorizer = CountVectorizer()
with open('spisok', 'r') as file:
    for line in file:
        if len(line) < 3:
            continue
        line_no_spaces = line.replace(' ', '')
        try:
            start = int(line_no_spaces[0])
        except:
            labels.append(line_no_spaces[:-1])
            continue

        for i in range(len(line)):
            if line[i] == ' ':
                continue
            if line[i] == '.':
                line = line[i+2:]
                break

        data_dict[line[:-1]] = len(labels)
        data.append(translit(u"{}".format(line[:-1]), "ru", reversed=True))
        label.append(len(labels))

data_vectorised = vectorizer.fit_transform(data)
print(data_vectorised.shape)
print(data_vectorised)
n_label = np.array(label)
print(n_label.shape)


trainX, testX, trainY, testY = train_test_split(data_vectorised, n_label, test_size = 0.1, random_state = 42)

trainY = to_categorical(trainY, num_classes=len(labels)+1)
testY = to_categorical(testY, num_classes=len(labels)+1)



from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten, Activation
from keras.layers.convolutional import MaxPooling2D
model = Sequential()

model.add(Dense(units=500, activation='relu', input_dim=len(vectorizer.get_feature_names())))
model.add(Dense(units=300, activation='relu'))
model.add(Dense(units=164, activation='relu'))

# softmax classifier
model.add(Dense(len(labels)+1))
model.add(Activation("softmax"))




model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])
model.fit(trainX, trainY, epochs=15)

score, acc = model.evaluate(testX, testY)
print(score, acc)

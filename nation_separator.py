from sklearn.feature_extraction.text import  TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from sklearn.pipeline import Pipeline
from transliterate import translit
import pickle

labels = []
data_dict = {}
data = []
label = []
vectorizer = CountVectorizer()
with open('modern_tech', 'r') as file:
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
print(labels)
n_label = np.array(label)


trainX, testX, trainY, testY = train_test_split(data_vectorised, n_label, test_size = 0.2, random_state = 42)

from sklearn import metrics
from sklearn.naive_bayes import MultinomialNB


nb_classifier = MultinomialNB(alpha=0.3)
nb_classifier.fit(trainX, trainY)
pred = nb_classifier.predict(testX)
score = metrics.accuracy_score(testY, pred)
print(score)
a = nb_classifier.predict(vectorizer.transform(['Panzer']))
print(a)
print()

from sklearn.linear_model import SGDClassifier

nb = Pipeline([


                ('clf', SGDClassifier(loss='hinge', penalty='l2',alpha=1e-3, random_state=42, max_iter=3, tol=None)),
              ])
nb.fit(trainX, trainY)
y_pred = nb.predict(testX)
a = nb_classifier.predict(vectorizer.transform(['AVGP Cougar']))
print(a)

print('accuracy %s' % metrics.accuracy_score(y_pred, testY))

filename = 'modern'
pickle.dump(nb, open(filename, 'wb'))
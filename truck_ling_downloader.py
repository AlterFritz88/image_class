import requests
from lxml.html import fromstring
import os
import random as rd
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from fitter_vocab import fitter_age, fitter_modern, fitter_WWII


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

model_modern = Pipeline([


                ('clf', SGDClassifier(loss='hinge', penalty='l2',alpha=1e-3, random_state=42, max_iter=3, tol=None)),
              ])
model_modern.fit(trainX, trainY)



model_age = pickle.load(open('age_model', 'rb'))
model_WWII = pickle.load(open('wwii', 'rb'))
#model_modern = pickle.load(open('modern', 'rb'))

vectorizer_age = CountVectorizer()
vectorizer_age.fit(fitter_age())

vectorizer_modern = CountVectorizer()
vectorizer_modern.fit(fitter_modern())

vectorizer_wwII = CountVectorizer()
vectorizer_wwII.fit(fitter_WWII())





labels_wwII = []
with open('spisok', 'r') as file:
    for line in file:
        if len(line) < 3:
            continue
        line_no_spaces = line.replace(' ', '')
        try:
            start = int(line_no_spaces[0])
        except:
            labels_wwII.append(line_no_spaces[:-1])
            continue

labels_modern = []
with open('modern_tech', 'r') as file:
    for line in file:
        if len(line) < 3:
            continue
        line_no_spaces = line.replace(' ', '')
        try:
            start = int(line_no_spaces[0])
        except:
            labels_modern.append(line_no_spaces[:-1])
            continue





#from 10000

for model_page in range(10036, 11001, 1):
    print(model_page)

    url = "https://www.track-link.com/gallery/{}".format(model_page)
    r = requests.get(url)
    tree = fromstring(r.content)
    path = ' '.join(tree.findtext('.//title').split(' ')[4:]).replace(r'/', ' ')
    print(path)
    if len(path) < 3:      # если в шапке пусто, то скипаем, чтобы не мусорить
        continue

    what_age = model_age.predict(vectorizer_age.transform([path]))
    if what_age == 0:
        age = 'WWII'
        nation = labels_wwII[model_WWII.predict(vectorizer_wwII.transform([path]))[0] - 1]
    else:
        age = 'Modern'
        nation = labels_modern[model_modern.predict(vectorizer.transform([path]))[0] - 1]
    print(age, nation)
    print()




    dirName = 'truck-link/{0}/{1}/{2}'.format(age, nation, path)

    if not os.path.exists('truck-link/{0}/{1}'.format(age, nation)):
        os.mkdir('truck-link/{0}/{1}'.format(age, nation))


    if not os.path.exists(dirName):
        os.mkdir(dirName)

    try:
        for i in range(10):
            image_url = "https://www.track-link.com/gallery/images/b_{0}_{1}.jpg".format(model_page, i)
            r = requests.get(image_url)
            filename = "truck-link/{0}/{1}/{2}/{3}.jpeg".format(age, nation, path, i)

            if os.path.isfile(filename):
                filename = 'truck-link/{0}/{1}/{2}/{3}.jpeg'.format(age, nation, path, i + rd.randint(10, 10000))
                with open(filename, 'wb') as f:
                    f.write(r.content)
            else:

                with open(filename, 'wb') as f:
                    f.write(r.content)
    except:
        continue

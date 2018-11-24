import os
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import  TfidfVectorizer
import random as rd

'''
кластеризует собранные данные по папкам и удаляет пустные
важно знать на сколько видов делить!!!!
работать с бэкапом данных!!!!
'''

li_dir = os.listdir(path="truck-link")

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(li_dir)
kmeans = KMeans(n_clusters=310).fit(X)
print(kmeans.labels_)

dick_paths = {}
for i in range(len(li_dir)):
    if kmeans.labels_[i] not in dick_paths.keys():
        dick_paths[kmeans.labels_[i]] = []
        dick_paths[kmeans.labels_[i]].append(li_dir[i])
    else:
        dick_paths[kmeans.labels_[i]].append(li_dir[i])
print(dick_paths)

for key, value in dick_paths.items():

    for i in range(len(value)):
        if i == 0:
            temp_path = 'truck-link/{0}/'.format(value[0])
            print('into', temp_path)

        else:
            for item in os.listdir('truck-link/{0}'.format(value[i])):
                sourse = 'truck-link/' + value[i] + '/' + item
                destin = temp_path + '{}'.format(rd.randint(10,100000))
                if os.stat(sourse).st_size < 25000:
                    os.remove(sourse)
                else:
                    os.rename(sourse,  destin)
            os.rmdir('truck-link/{0}'.format(value[i]))
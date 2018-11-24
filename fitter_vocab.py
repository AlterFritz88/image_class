def fitter_age():
    from sklearn.feature_extraction.text import CountVectorizer
    from transliterate import translit

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
                    line = line[i + 2:]
                    break

            if len(labels) == 2 or len(labels) == 7:
                data_dict[translit(u"{}".format(line[:-1]), "ru", reversed=True)] = len(labels)
                data.append(translit(u"{}".format(line[:-1]), "ru", reversed=True))
                label.append(0)
                continue
            data_dict[line[:-1]] = len(labels)
            data.append(line[:-1])
            label.append(0)

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
                    line = line[i + 2:]
                    break

            data_dict[translit(u"{}".format(line[:-1]), "ru", reversed=True)] = len(labels)
            data.append(translit(u"{}".format(line[:-1]), "ru", reversed=True))
            label.append(1)

    return data

def fitter_WWII():
    from sklearn.feature_extraction.text import CountVectorizer
    from transliterate import translit

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
                    line = line[i + 2:]
                    break

            if len(labels) == 2 or len(labels) == 7:
                data_dict[translit(u"{}".format(line[:-1]), "ru", reversed=True)] = len(labels)
                data.append(translit(u"{}".format(line[:-1]), "ru", reversed=True))
                label.append(len(labels))
                continue
            data_dict[line[:-1]] = len(labels)
            data.append(translit(u"{}".format(line[:-1]), "ru", reversed=True))
            label.append(len(labels))
    return data

def fitter_modern():
    from sklearn.feature_extraction.text import CountVectorizer
    from transliterate import translit

    labels = []
    data_dict = {}
    datam = []
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
                    line = line[i + 2:]
                    break

            if len(labels) == 2 or len(labels) == 7:
                data_dict[translit(u"{}".format(line[:-1]), "ru", reversed=True)] = len(labels)
                datam.append(translit(u"{}".format(line[:-1]), "ru", reversed=True))
                label.append(0)
                continue
            data_dict[line[:-1]] = len(labels)
            datam.append(line[:-1])
            label.append(0)
    return datam
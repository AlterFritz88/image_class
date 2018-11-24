import os
'''
li_dir = os.listdir(path="truck-link")
for dir in li_dir:
    if len(dir) > 20:
        os.replace("truck-link/{0}".format(dir), "truck-link/{0}".format(dir[:20]))
'''
li_dir = os.listdir(path="truck-link")
for dir in li_dir:
    files = os.listdir(path="truck-link/{}".format(dir))
    print(files)
    for file in files:
        size = os.stat("truck-link/{0}/{1}".format(dir, file)).st_size
        if size < 25000:
            os.remove("truck-link/{0}/{1}".format(dir, file))
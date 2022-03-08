import os

for file_name in os.listdir("data/interim_samples/"):
    file_path = "data/interim_samples/"+file_name
    data = [float(e) for e in open(file_path).readlines() if 5 > float(e) > -5]

    if len(data) == 1:
        os.remove(file_path)
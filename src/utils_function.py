import numpy as np


# Load the brainwaves file from its standard format and loads its data in a numpy array
# path (string): path of the desired file
def load_brainwaves(path):
    return np.array([float(e) for e in open(path, 'r').readlines()])


# Saves a numpy array as a brainwaves file, in its standard format
# path (string): path where to save the file
# data (float64[]): data to save
def save_brainwaves(path, data):
    open(path, 'w').writelines("\n".join(data.astype("str")))

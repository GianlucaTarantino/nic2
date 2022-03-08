import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import os

all_data = []

#fig, axs = plt.subplots(5, 3, )
#r, c = 0, 0


for file_name in os.listdir("data/interim_samples/"):
    file_path = "data/interim_samples/"+file_name
    data = np.array([float(e) for e in open(file_path).readlines() if 5 > float(e) > -5])

    resampled = signal.resample(data, 100)
    normalized = (resampled-min(resampled))/(max(resampled)-min(resampled))

    #axs[r][c].plot(list(range(100)), normalized)
    '''
    r += 1
    if r == 5:
        c += 1
        r = 0
    '''
    all_data.append(normalized)

plt.show()

mean_array = np.mean(all_data, axis=0)

open("data/samples/arm_open_sample.csv", "w").write("\n".join([str(el) for el in mean_array]))

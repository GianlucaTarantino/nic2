import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Paths of signal and sample data
data_file_name = "15-Jan-2022T12:39:43.778054_3_T.csv"
data_file_path = "/home/gianluca/Programmazione/Progetti/BCI/data/processed/" + data_file_name
sample_file_name = "15-Jan-2022T12:30:19.608124_3_L_sample_1.csv"
sample_file_path = "/home/gianluca/Programmazione/Progetti/BCI/data/samples/" + sample_file_name

# Getting signal and sample data as numpy arrays
data = np.array([float(e) for e in open(data_file_path).readlines()])
sample = np.array([float(e) for e in open(sample_file_path).readlines()])

# Cross-correlating signal with the sample and getting the peaks
correlated = signal.correlate(data, sample, mode="same", method="fft")
correlated_peaks, _ = signal.find_peaks(data, distance=10)

# Array for the peaks that are recognized to be from a movement
recognized = []

# Getting only peaks of the correlation that are in a zone that has a mean value bigger than the normal mean value of the signal of the same
for p in correlated_peaks:
    if np.mean(correlated[max(0, p-10):min(len(data), p+10)]) > np.mean(data[max(0, p-10):min(len(data), p+10)])+0.02:
        recognized.append(p)

# Getting the highest peak for each second
for s in range(1, 11):
    max_peak_s = -np.inf
    max_peak_i = -1
    for i in range(250*(s-1), 250*s):
        if i in recognized and correlated[i] > max_peak_s:
            max_peak_s = correlated[i]
            max_peak_i = i
    for i in range(250 * (s - 1), 250 * s):
        if i in recognized and i != max_peak_i:
            recognized.pop(recognized.index(i))

# Plotting the correlated signal with crosses over recognized peaks
plt.ylim(-0.2, 0.2)
plt.plot(correlated)
plt.plot(recognized, correlated[recognized], 'x')
plt.show()


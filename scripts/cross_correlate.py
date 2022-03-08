import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

# Getting signal and sample data as numpy arrays
data = np.array([float(e) for e in open("data/processed/id03_r01_19_Feb_2022T10_55_14_319653.csv").readlines()])
sample = np.array([float(e) for e in open("data/samples/arm_open_sample.csv").readlines()])

# Cross-correlating signal with the sample and getting the peaks
correlated = signal.correlate(data, sample, mode="same", method="fft")
correlated = (correlated-min(correlated))/(max(correlated)-min(correlated))

correlated_peaks, _ = signal.find_peaks(correlated, prominence=0.65, width=(0, 140), rel_height=0.5)
plt.plot(correlated)
#plt.plot(correlated_peaks, correlated[correlated_peaks], 'x')
plt.show()

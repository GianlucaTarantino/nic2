import numpy as np
from scipy import signal

import os

for file_name in os.listdir("data/raw/"):
    file_path = "data/raw/"+file_name
    data = np.array([float(e) for e in open(file_path).readlines() if 5 > float(e) > -5])

    sample_rate = 250.0  # Samples rate in Hz
    nyq = 0.5 * sample_rate

    cutoff_low = 15.0  # Frequency of the low pass filter
    cutoff_high = 0.4  # Frequency of the high pass filter
    frequency_notch = 50  # Frequency of the notch filter

    # Applying low pass filter to remove certain frequencies lower than a threshold
    # noinspection PyTupleAssignmentBalance
    low_filtered_b, low_filtered_a = signal.butter(1, cutoff_low / nyq, btype='low')
    low_filtered = signal.filtfilt(low_filtered_b, low_filtered_a, data)

    # Applying high pass filter to level the signal
    # noinspection PyTupleAssignmentBalance
    high_filtered_b, high_filtered_a = signal.butter(1, cutoff_high / nyq, btype='high')
    high_filtered = signal.filtfilt(high_filtered_b, high_filtered_a, low_filtered)

    # Applying notch filter, to remove 50hz from signal
    notch_filtered_b, notch_filtered_a = signal.iirnotch(frequency_notch, 30.0, sample_rate)
    notch_filtered = signal.filtfilt(notch_filtered_b, notch_filtered_a, high_filtered)

    open("data/processed/" + file_name, "w").write("\n".join(notch_filtered.astype("str")))

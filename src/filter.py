from utils_function import load_brainwaves, save_brainwaves
from scipy import signal

data = load_brainwaves("/home/gianluca/Programmazione/Progetti/BCI/data/raw/AcquiredBrainWave_2022-01-05_21-47-11.csv")

period = 4.0  # Total period of time of the detected signal
sample_rate = 250.0  # Samples rate in Hz
samples_number = int(period * sample_rate)  # Total number of samples in the period time
nyq = 0.5 * sample_rate

cutoff_low = 20  # Frequency of the low pass filter
cutoff_high = 0.3  # Frequency of the high pass filter
frequency_notch = 50  # Frequency of the notch filter

# Applying low pass filter to remove certain frequencies lower than a threshold
low_filtered_b, low_filtered_a = signal.butter(1, cutoff_low/nyq, btype='low', analog=False)
low_filtered = signal.filtfilt(low_filtered_b, low_filtered_a, data)
# Applying high pass filter to level the signal
high_filtered_b, high_filtered_a = signal.butter(1, cutoff_high/nyq, btype='high', analog=False)
high_filtered = signal.filtfilt(high_filtered_b, high_filtered_a, low_filtered)
# Applying notch filter, to remove 50hz from signal
notch_filtered_b, notch_filtered_a = signal.iirnotch(frequency_notch, 30.0, sample_rate)
notch_filtered = signal.filtfilt(notch_filtered_b, notch_filtered_a, high_filtered)

save_brainwaves("/home/gianluca/Programmazione/Progetti/BCI/data/processed/AcquiredBrainWave_2022-01-05_21-47-11.csv",
                notch_filtered)

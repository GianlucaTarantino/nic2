import numpy as np
from scipy import signal

"""
Module with all the functions useful for the detection, processing and recognition of brainwaves signals.
"""

def is_float(element: str) -> bool:
    try:
        float(element)
        return True
    except ValueError:
        return False

def filter(data: np.ndarray, sample_rate: float = 250.0, cutoff_low: float = 5.0, cutoff_high: float = 0.4, frequency_notch: float = 50.0) -> np.ndarray:

    """
    Filters the signal passed as parameter in data and returns the filtered signal.
    Applied filters are high pass, low pass and notch filter.

    Keyword arguments:
    data -- the input signal to filter. Must be a 1 dimensional array of values. Also numpy array are accepted
    sample_rate -- rate in Hz of the signal  (default 250.0)
    cutoff_low -- the cutoff of the low pass filter. The smaller, the more aggressive is the filter (default 5.0)
    cutoff_high -- the cutoff of the high pass filter. The smaller, the more aggressive is the filter (default 0.4)
    frequency_notch -- the frequency in Hz to cut from the signal with the notch filter (default frequency_notch 50.0)
    
    Returns:
    1 dimensional numpy array with the filtered values of the signal
    """

    # Calculating Nyquist frequency
    nyq = 0.5*sample_rate

    # Applying low pass filter to remove certain frequencies lower than a threshold
    low_filtered_b, low_filtered_a = signal.butter(1, cutoff_low / nyq, btype='low')
    low_filtered = signal.filtfilt(low_filtered_b, low_filtered_a, data)

    # Applying high pass filter to level the signal
    high_filtered_b, high_filtered_a = signal.butter(1, cutoff_high / nyq, btype='high')
    high_filtered = signal.filtfilt(high_filtered_b, high_filtered_a, low_filtered)

    # Applying notch filter, to remove 50hz from signal
    notch_filtered_b, notch_filtered_a = signal.iirnotch(frequency_notch, 30.0, sample_rate)
    notch_filtered = signal.filtfilt(notch_filtered_b, notch_filtered_a, high_filtered)

    return notch_filtered

def recognize(data: np.ndarray, sample: np.ndarray, seconds: float = 2.0, sample_rate: float = 250.0) -> np.ndarray:

    """
    Function used to cross-correlate two signal and finding the peaks of the correlated signal so that it should recognize if the second signal is in the first

    Keyword Arguments: 
    data -- the main signal, in which to find the signal contained in sample. Must be 1 dimensional array of numbers
    sample -- the sample of the signal to recognize in the first signal. Must be 1 dimensional array of numbers
    seconds -- the duration in seconds of the main signal (default 2.0)
    sample_rate -- the number of samples for second in the main signal. In Hz (default 250.0)
    
    Returns:
    tuple with an array of all the recognized peaks as first element and numpy array with the cross-correlated signals as second element
    """

    # Array for the peaks that are recognized to be from a movement
    recognized = []

    # Cross-correlating signal with the sample and getting the peaks
    correlated = signal.correlate(data, sample, mode="same", method="fft")
    correlated_peaks, _ = signal.find_peaks(correlated, distance=10)

    # Getting only peaks of the correlation that are in a zone that has a mean value bigger than the normal mean value of the signal of the same
    for p in correlated_peaks:
        if np.mean(correlated[max(0, p-10):min(len(data), p+10)]) > np.mean(data[max(0, p-10):min(len(data), p+10)])+0.02:
            recognized.append(p)

    # Getting the highest peak for each second
    for s in range(1, seconds + 1):
        max_peak_s = -np.inf
        max_peak_i = -1
        for i in range(sample_rate*(s-1), sample_rate*s):
            if i in recognized and correlated[i] > max_peak_s:
                max_peak_s = correlated[i]
                max_peak_i = i
        for i in range(sample_rate * (s - 1), sample_rate * s):
            if i in recognized and i != max_peak_i:
                recognized.pop(recognized.index(i))
    
    return (recognized, correlated)

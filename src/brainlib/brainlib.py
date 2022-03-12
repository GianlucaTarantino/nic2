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

def filter(data: np.ndarray, sample_rate: float = 250.0, cutoff_low: float = 15.0, cutoff_high: float = 0.35, frequency_notch: float = 50.0) -> np.ndarray:

    """
    Filters the signal passed as parameter in data and returns the filtered signal.
    Applied filters are high pass (to remove all frequencies over a certain threshold), 
    low pass (to remove all frequencies over a certain threshold) and notch (to remove the frequency of the specified value) filter.

    Keyword arguments:
    data -- the input signal to filter. Must be a 1 dimensional array of values. Also numpy array are accepted
    sample_rate -- rate in Hz of the signal  (default 250.0)
    cutoff_low -- the cutoff frequency of the low pass filter. All frequencies over this value are removed (default 15.0)
    cutoff_high -- the cutoff frequency of the high pass filter. All frequencies under this value are removed (default 0.35)
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

def correlate_peaks(data: np.ndarray, samples: np.ndarray) -> list:

    """
    Function used to cross-correlate two signals and to find the peak characteristics of the correlated signal. 
    It takes multiple samples, and returns a list of indexes of recognized signals.
    It recognizes a signal based on the prominence of the peak (that has to be a minimum of 0.65) and the 
    width of the peak (that has to be a maximum of 140)

    Keyword Arguments: 
    data -- the main signal, in which to find the signal contained in sample. Must be 1 dimensional array of numbers
    samples -- the array with all the samples, of which will be returned the index of the most similar sample
    
    Returns:
    list with indexes of recognized peaks
    """

    # Normalize data
    data = (data-min(data))/(max(data)-min(data))

    detected_samples = []

    for i in range(len(samples)):
        sample = samples[i]

        # Get correlated signal
        correlated = signal.correlate(data, sample, mode="same", method="fft")
        # Normalize correlated signal
        correlated = (correlated-min(correlated))/(max(correlated)-min(correlated))
        # Get all peaks from correlated signal
        correlated_peaks, _ = signal.find_peaks(correlated, prominence=0.84, width=(0, 109), rel_height=0.5)

        # If there is any peak with the above characteristics, then the peak is added to the array to return
        if len(correlated_peaks) > 0:
            detected_samples.append(i)
    
    return detected_samples

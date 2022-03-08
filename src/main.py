import time
import serial
import pydobot
import numpy as np
from brainlib.brainlib import is_float, filter, correlate_peaks

MODE_DEBUG = True

# Serial devices configuration
ser = serial.Serial('/dev/ttyACM0', 115200)
if not MODE_DEBUG:
    arm = pydobot.Dobot("/dev/ttyUSB0")

# Defining detection variables
current_signal = []
move_arm = True

# Configuration variables
max_signal_length = 5000
mean_sensibility = 0.005

# Importing samples file
samples = (
    np.array([float(e) for e in open("data/samples/arm_open_sample.csv").readlines()]),
)

while 1:
    
    # Reading new value sent from serial ADS1299
    serial_value = ser.readline()

    # Checking if data is valid (is not garbage serial bits and is not too high or low)
    if not is_float(serial_value) or (float(serial_value) > 5 or float(serial_value) < -5):
        continue

    # If so, append the current detected sample to the signal array
    current_signal.append(float(serial_value))

    # Cutting the signal if too long to save memory
    if len(current_signal) < 2000:
        print("Wait", end='\r')
        continue
    elif len(current_signal) > 5000:
        current_signal = current_signal[2500:]

    # Getting the filtered signal to apply cross-correlation on it with all the samples and making checks of the mean value
    filtered_signal = filter(current_signal)

    # Checking if the mean value of the last second of the signal is outside the sensibility range. If so, something has been detected.
    if -mean_sensibility < np.mean(filtered_signal[-250:]) < mean_sensibility:
        print("Still | "+str(np.mean(filtered_signal[-250:])), end='\r')
        continue

    similar_samples = correlate_peaks(filtered_signal[:500], samples)

    for sample in similar_samples:
        if sample == 1:
            print("Move right | "+str(np.mean(filtered_signal[-250:])), end='\r')

    print('\r', end='')
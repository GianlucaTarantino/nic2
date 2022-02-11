import time
import serial
import pydobot
import numpy as np
from brainlib.brainlib import is_float, filter, recognize

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
mean_sensibility = 0.0

# Importing samples file
open_arm_sample = np.array([float(e) for e in open("/home/gianluca/Programmazione/Progetti/BCI/data/samples/"
                                                        "sample_arm_in.csv").readlines()])
closed_arm_sample = np.array([float(e) for e in open("/home/gianluca/Programmazione/Progetti/BCI/data/samples/"
                                                        "sample_arm_out.csv").readlines()])

while 1:
    
    # Reading new value sent from serial ADS1299
    serial_value = ser.readline()

    # Checking if data is valid (is not garbage serial bits and is not too high or low)
    if not is_float(serial_value) or (float(serial_value) > 5 or float(serial_value) < -5):
        continue

    # If so, append the current detected sample to the signal array
    current_signal.append(float(serial_value))

    # Cutting the signal if too long to save memory
    if len(current_signal) < 500:
        continue
    elif len(current_signal) > 5000:
        current_signal = current_signal[2500:]

    # Getting the filtered signal to apply cross-correlation on it with all the samples and making checks of the mean value
    filtered_signal = filter(current_signal)

    # Checking if the mean value of the last second of the signal is outside the sensibility range. If so, something has been detected.
    if -mean_sensibility < np.mean(filtered_signal[-250:]) < mean_sensibility:
        print(np.mean(filtered_signal[-250:]), end='\r')
        continue

    # Applying cross correlation to the current signal with every available sample and getting the recognized peaks and the correlated signal.
    recognized_open_arm, correlated_open_arm = recognize(filtered_signal, open_arm_sample)
    recognized_closed_arm, correlated_closed_arm = recognize(filtered_signal, closed_arm_sample)
    
    # Moving the robotic arm if connected and if a movement is ongoing
    if move_arm and not MODE_DEBUG:
        (x, y, z, r, j1, j2, j3, j4) = arm.pose()
        arm.move_to(x - 3, y - 10, z, r)

    # Checking if there are recognized peaks in the last second of the signal and if the mean value of the correlated signal \
    # with a sample is bigger of all the other correlations
    if [e for e in recognized_open_arm if e >= len(current_signal)-250] and np.mean(correlated_open_arm[-250:]) >= np.mean(correlated_closed_arm[-250:]):
        print("Opened", end='\r')
        move_arm = True
    elif [e for e in recognized_closed_arm if e >= len(current_signal)-250] and np.mean(correlated_closed_arm[-250:]) >= np.mean(correlated_open_arm[-250:]):
        print("Closed", end='\r')
        move_arm = False
    else:
        print("Still ", end='\r')

    print('\r', end='')
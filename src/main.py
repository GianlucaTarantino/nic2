import time
import serial
import pydobot
import numpy as np
from brainlib.brainlib import is_float, filter, correlate_peaks

DOBOT = False
arm = 0

# Serial devices configuration
ser = serial.Serial('/dev/ttyACM0', 115200)
if DOBOT:
    arm = pydobot.Dobot("/dev/ttyUSB0")
    arm.suck(True)
    arm.grip(False)

# Defining detection variables
current_signal_l, current_signal_r = [], []
move_arm = True
grip = False
last_grip = -1
last_move = -1
brain_value_l, brain_value_r, eeg_value = 0.0, 0.0, 0

# Configuration variables
max_signal_length = 5000
mean_sensibility = 0.0

# Importing samples file
samples = (
    np.array([float(e) for e in open("data/samples/arm_open_sample.csv").readlines()]),
)

while 1:
    
    # Reading new value sent from serial ADS1299
    try:
        values = (ser.readline().decode("utf-8").strip(), ser.readline().decode("utf-8").strip(), ser.readline().decode("utf-8").strip())
        for value in values:
            if value[0] == "E":
                eeg_value = int(value[1:])
            elif value[0] == "L":
                brain_value_l = float(value[1:])
            elif value[0] == "R":
                brain_value_r = float(value[1:])
    except Exception as e:
        print(e, "brain_l: ", brain_value_l, "brain_r", brain_value_r, "eeg: ", eeg_value)
        continue

    # Checking if data is valid (is not garbage serial bits and is not too high or low)
    if not is_float(brain_value_l) or (float(brain_value_l) > 10 or float(brain_value_l) < -10):
        print("Invalid value: "+str(brain_value_l), end='\r')
        continue

    # If so, append the current detected sample to the signal array
    current_signal_l.append(float(brain_value_l))
    current_signal_r.append(float(brain_value_r))

    # Cutting the signal if too long to save memory (left signal)
    if len(current_signal_l) < 1000:
        print(f"Wait (length of signal: {len(current_signal_l)} samples)", end='\r')
        continue
    elif len(current_signal_l) > 5000:
        current_signal_l = current_signal_l[2500:]

    # Cutting the signal if too long to save memory (right signal)
    if len(current_signal_l) < 1000:
        print(f"Wait (length of signal: {len(current_signal_l)} samples)", end='\r')
        continue
    elif len(current_signal_l) > 5000:
        current_signal_l = current_signal_l[2500:]

    # Getting the filtered signal to apply cross-correlation on it with all the samples and making checks of the mean value
    filtered_signal_l = filter(current_signal_l)
    filtered_signal_r = filter(current_signal_r)

    print("Detecting... | L"+str(np.mean(filtered_signal_l[-250:])), "R", str(np.mean(filtered_signal_r[-250:])), "E", str(eeg_value), end='\r')

    similar_samples_l = correlate_peaks(filtered_signal_l[-250:], samples)
    similar_samples_r = correlate_peaks(filtered_signal_r[-250:], samples)

    # Recognized samples in the left signal
    for sample in similar_samples_l:
        if sample == 0 and time.time()-last_move > 1.5:
            print("Move right arm | "+str(np.mean(filtered_signal_l[-250:]))+"____________________ DETECTED"+str(time.time()))
            last_move = time.time()
            if DOBOT:
                (x, y, z, r, j1, j2, j3, j4) = arm.pose()
                arm.move_to(x - 10, y - 40, z, r)
    # Recognized samples in the right signal
    for sample in similar_samples_r:
        if sample == 0 and time.time()-last_move > 1.5:
            print("Move left arm | "+str(np.mean(filtered_signal_r[-250:]))+"____________________ DETECTED"+str(time.time()))
            last_move = time.time()
            if DOBOT:
                (x, y, z, r, j1, j2, j3, j4) = arm.pose()
                arm.move_to(x - 10, y + 40, z, r)
    
    if eeg_value > 140 and time.time()-last_grip > 1.5:
        print("Grip | "+str(eeg_value))
        grip = not grip
        arm.grip(grip)
        last_grip = time.time()

    print('\r', end='')

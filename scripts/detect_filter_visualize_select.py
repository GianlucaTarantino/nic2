from fileinput import filename
import time
import numpy as np
import serial
from datetime import datetime
import matplotlib.pyplot as plt
from scipy import signal

def isfloat(element) -> bool:
    try:
        float(element)
        return True
    except ValueError:
        return False

# Setting serial communication with ACM1299
ser = serial.Serial('/dev/ttyACM0', 115200)

# Configuration variables
relevation_time = 30 # time in seconds of the relevation

# Utils variables
y = [] # storing all the detected values
now = time.time() # current time to know when to stop the countdown

# Countdown to let the user get prepared after running the program
print("Relevation time:", relevation_time)
while time.time()-now <= 5:
    print(str(5-int(time.time()-now))+"...", end='\r')
    time.sleep(0.7)

now = time.time() # getting current time to know when to stop the detection
while time.time()-now <= relevation_time:
    
    # Getting value from serial and printing it
    value = ser.readline()
    print(value, " | ", time.time()-now, " | ", len(y), end='\r')
    
    # Skipping if the value isn't valid
    if not isfloat(value) or (float(value) > 2 or float(value) < -2):
        continue

    # Appending value to the array of the signal if valid
    y.append(float(value))

# Configuration variables
sample_rate = 250.0  # Samples rate in Hz
nyq = 0.5 * sample_rate
cutoff_low = 5  # Frequency of the low pass filter
cutoff_high = 0.4  # Frequency of the high pass filter
frequency_notch = 50  # Frequency of the notch filter

# Applying low pass filter to remove certain frequencies lower than a threshold
low_filtered_b, low_filtered_a = signal.butter(1, cutoff_low / nyq, btype='low')
low_filtered = signal.filtfilt(low_filtered_b, low_filtered_a, y)

# Applying high pass filter to level the signal
high_filtered_b, high_filtered_a = signal.butter(1, cutoff_high / nyq, btype='high')
high_filtered = signal.filtfilt(high_filtered_b, high_filtered_a, low_filtered)

# Applying notch filter, to remove 50hz from signal
notch_filtered_b, notch_filtered_a = signal.iirnotch(frequency_notch, 30.0, sample_rate)
notch_filtered = signal.filtfilt(notch_filtered_b, notch_filtered_a, high_filtered)

# Visualizing the just detected data
plt.plot(notch_filtered)
plt.show()

print(' '*100, end='\r')
# Choosing if to save the relevation or not
user_value = input("Want to save detection? (Y/n) ").strip()
if user_value == "" or user_value.upper() == "Y":

    # Saving raw and filtered file with timestamp and asking user for the file classification string
    file_name = f"{input('Insert file classification: ')}_{datetime.now().strftime('%d-%b-%YT%H:%M:%S:%f')}.csv"
    open("/home/gianluca/Programmazione/Progetti/BCI/data/raw/" + file_name, "w").write(
            "\n".join([str(e) for e in y]))
    open("/home/gianluca/Programmazione/Progetti/BCI/data/processed/" + file_name, "w").write(
            "\n".join(notch_filtered.astype("str")))
import time
import serial
from datetime import datetime

def isfloat(element) -> bool:
    try:
        float(element)
        return True
    except ValueError:
        return False

# Setting serial communication with ACM1299
ser = serial.Serial('/dev/ttyACM0', 115200)

# Configuration variables
relevation_time = 10 # time in seconds of the relevation

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
    print(value, " | ", time.time()-now, end='\r')
    
    # Skipping if the value isn't valid
    if not isfloat(value):
        continue

    # Appending value to the array of the signal if valid
    y.append(float(value))

# Saving file with timestamp and asking user for the file classification string
open(f"/home/gianluca/Programmazione/Progetti/BCI/data/raw/{input('Insert file classification: ')}_{datetime.now().strftime('%d-%b-%YT%H:%M:%S.%f')}.csv", "w").write("\n".join([str(e) for e in y]))


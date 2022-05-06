import serial
import time
ser = serial.Serial(port='COM7', baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1.0)

input()

ser.write(b'1')
time.sleep(11)
ser.write(b'0')
time.sleep(30)
ser.write(b'1')
time.sleep(30)
ser.write(b'0')
ser.close()
import pydobot
arm = pydobot.Dobot("/dev/ttyUSB0")
arm.grip(False)
arm.suck(False)
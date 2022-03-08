import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

file_name = input("Insert file name of the CSV to cut: ")
file_path = "data/processed/"+file_name
data = np.array([float(e) for e in open(file_path).readlines() if 5 > float(e) > -5])

seconds = [1, 4, 8, 11, 14, 17]
eu = [0, 0, 0, 0, 0, 0]


for i in range(len(seconds)):
    print("Apertura" if eu[i] == 0 else "Chiusura")
    plt.plot(data[(seconds[i]-1)*250:(seconds[i]+1)*250])
    plt.show()

    number1 = int(input("Insert first index to cut: "))
    number2 = int(input("Insert second index to cut: "))

    currsample = data[(seconds[i]-1)*250+number1:(seconds[i]-1)*250+number2]

    if len(currsample) > 1:
        open(f"data/interim_samples/s{i+1}_{file_name}" + file_name, "w").write("\n".join(currsample.astype("str")))

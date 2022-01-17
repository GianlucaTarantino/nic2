import matplotlib.pyplot as plt

data = [float(e) for e in open("/home/gianluca/Programmazione/Progetti/BCI/data/processed/"
                               "15-Jan-2022T12:24:56.478956_1_L.csv").readlines()]

plt.plot(data)
plt.show()

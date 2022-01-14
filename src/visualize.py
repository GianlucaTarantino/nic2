from utils_function import load_brainwaves
import matplotlib.pyplot as plt

data = load_brainwaves("/home/gianluca/Programmazione/Progetti/BCI/data/processed/AcquiredBrainWave_2022-01-05_21-47-11.csv")

plt.plot(data)
plt.show()

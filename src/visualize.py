from utils_function import load_brainwaves
import matplotlib.pyplot as plt

data = load_brainwaves("/home/gianluca/Programmazione/Progetti/BCI/data/processed/AcquiredBrainWave_2022-01-10_07-03-02_Alzati.csv")

plt.plot(data)
plt.show()

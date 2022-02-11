import matplotlib.pyplot as plt

# Getting data from file as numpy array and not plotting values too big or too small
data = [float(e) for e in open("/home/gianluca/Programmazione/Progetti/BCI/data/processed/"+input("Insert file name of the CSV to visualize: ")).readlines() 
        if float(e) < 5 and float(e) > -5]

# Plotting data
plt.plot(data)
plt.show()
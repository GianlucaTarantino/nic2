p = np.polyfit(list(range(100)), mean_data, 18)
polyfit = np.poly1d(p) 

plt.plot(mean_data)
plt.plot(polyfit(list(range(100))))
plt.show()
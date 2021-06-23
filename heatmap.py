import numpy as np
import matplotlib.pyplot as plt

x = np.random.rayleigh(1.0, size=50)
y = np.random.rayleigh(1.0, size=50)

print(x)
print(y)


plt.hist2d(x,y, bins=[np.arange(-2,2,0.2),np.arange(-2,2,0.2)])

plt.show()
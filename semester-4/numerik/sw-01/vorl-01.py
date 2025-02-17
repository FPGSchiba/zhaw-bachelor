import math
import numpy as np
from matplotlib import pyplot as plt

print(math.sin(math.radians(30)))

m = np.eye(50)

m = m - 1
m = abs(m * -1)

print(m)

x = np.linspace(0, 20, 100)
y1 = np.sin(x) / np.sqrt(x + 1)
y2 = np.sin(x / 2) / np.sqrt(x + 1)
y3 = np.sin(x / 3) / np.sqrt(x + 1)
plt.xlabel("x")
plt.plot(x, y1, "blue", x, y2, "red", x, y3, "orange")
plt.legend(["y1", "y2", "y3"])
# plt.show()

fig, axs = plt.subplots(1, 2)
fig.suptitle("Vertically stacked subplots")
x = np.linspace(0, 2 * math.pi, 100)
y = np.sin(x)
axs[0].plot(x, y, color="red")
axs[1].plot(x, -y, color="blue")


# plt.show()

def pythag(a, b):
    return np.sqrt(a ** 2 + b ** 2)


for i in range(1, 10):
    if pythag(3 * i, 4 * i) != 5 * i:
        print("Fehler")


import numpy as np
from matplotlib import pyplot as plt
import math

# 01
"""
t = np.linspace(0, 2*math.pi, 100)
x = np.cos(t)
y = np.sin(t)

plt.plot(x, y)
plt.show()
"""

# 02
"""
def plot_circle(a, b):
    t = np.linspace(a, b, 100)
    x = np.cos(t)
    y = np.sin(t)

    plt.plot(x, y)
    plt.show()

plot_circle(0, 2*math.pi)
"""


# 03
def plot_fancy_circle(A, a, B, b):
    t = np.linspace(0, 2 * math.pi, 100)
    x = np.cos(A * t + a)
    y = np.sin(B * t + b)

    plt.plot(x, y)
    plt.show()

plot_fancy_circle(2, 1, 0.5, 100)


# 04
plot_fancy_circle(2, math.pi / 4, 1, 0)
plot_fancy_circle(3, math.pi / 2, 1, 0)
plot_fancy_circle(1, 0, 1, 0)

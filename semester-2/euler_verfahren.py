import math
import time

from matplotlib import pyplot as plt
from tqdm import tqdm

h = 0.001
x0 = 0
f0 = 0

n = 20000

folgen = [(x0, f0)]


def G(x, f):
    return math.cos(x + f) + math.sin(x - f)


last_f = f0
last_x = x0

iter = tqdm(range(1, n + 1))

output = ''

for i in iter:
    fi = last_f + h * G(last_x, last_f)
    xi = last_x + h
    folgen.append((xi, fi))
    output += f'X{i} = {xi}\n'
    output += f'F{i} = {fi}\n'
    last_f = fi
    last_x = xi


plt.plot(*zip(*folgen))
plt.show()

print(output)

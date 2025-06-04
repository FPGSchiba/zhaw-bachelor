import numpy as np
import matplotlib.pyplot as plt

# Data
x = np.array([0, 1, 2, 3, 4])
y = np.array([6, 12, 30, 80, 140])

# Design matrix
A = np.column_stack((np.exp(x), np.ones_like(x)))

# Normal equations
ATA = A.T @ A
ATb = A.T @ y
params = np.linalg.solve(ATA, ATb)
a, c = params

# Fitted function
x_fit = np.linspace(1, 5, 100)
y_fit = a * np.exp(x_fit) + c

# Plot
plt.scatter(x, y, color='red', label='Data')
plt.plot(x_fit, y_fit, label='Fitted $f(x) = a \exp(x) + c$')
plt.legend()
plt.xlabel('x')
plt.ylabel('y')
plt.title('Least Squares Fit')
plt.show()

print(f"a = {a}, c = {c}")
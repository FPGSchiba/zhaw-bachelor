import numpy as np

def newton_steps(f, f1, x0, n=10):
    x = x0
    for i in range(n):
        x = x - f(x) / f1(x)
        print(x, i+1)
    return x

def newton_tol(f, f1, x0, tol=1.e-10):
    x = x0
    i = 0
    while abs(f(x)) > tol and i < 100:
        i += 1
        x = x - f(x) / f1(x)
        print(x, i)
    return x

result = newton_steps(lambda x: 2*x*np.sin(x) + x**2*np.cos(x), lambda x: 2*np.sin(x) + 4*x*np.cos(x) - x**2*np.sin(x), 5)
print(result)
result = newton_tol(lambda x: 2*x*np.sin(x) + x**2*np.cos(x), lambda x: 2*np.sin(x) + 4*x*np.cos(x) - x**2*np.sin(x), 5)
print(result)
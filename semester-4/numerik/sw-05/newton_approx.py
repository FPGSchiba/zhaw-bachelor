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

result = newton_steps(lambda x: x**2 - 3, lambda x: 2*x, 1)
print(result)
result = newton_tol(lambda x: x**2 - 3, lambda x: 2*x, 2)
print(result)

result = newton_tol(lambda x: 1+np.tan(x)**2 - np.exp(x), lambda x: 2*np.tan(x) + 2*np.tan(x)**3 - np.exp(x), 0.8)
print(result)



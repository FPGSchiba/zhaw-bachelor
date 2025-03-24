import numpy as np

def newton(f, J, x0, tol=1.e-10):
    max_loops = 1000
    x = x0
    k = 0
    res = np.linalg.norm(f(x))
    while res > tol and k < max_loops:
        k += 1
        d = np.linalg.solve(J(x), f(x))
        x = x - d
        res = np.linalg.norm(f(x))
    return x, k

f = lambda x: (x[0]**2 + x[0]*x[1]**3 - 9, 3*x[0]*x[1] - x[1]**3 - 4)
J = lambda x: np.array([[2*x[0] + x[1]**3, 3*x[0]*x[1]**2], [6*x[0]*x[1], 3*x[0]**2 - 3*x[1]**2]])

x0 = np.array([3, -1])
print(f"{x0}: {newton(f, J, x0)}")

x1 = np.array([1, 2])
print(f"{x1}: {newton(f, J, x1)}")

x2 = np.array([1, -1.5])
print(f"{x2}: {newton(f, J, x1)}")

x3 = np.array([0.9, -2.1])
print(f"{x3}: {newton(f, J, x1)}")
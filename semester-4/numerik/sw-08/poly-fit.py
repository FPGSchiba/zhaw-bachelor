import numpy as np

# Generiere kompliziertere Beispielfunktion
x = np. linspace ( -2.5, 2.5, 50 )
y = np. tanh(x) .reshape (-1,1)
# Ansatz: p3(x) = a + b*x + c*x^2 + d*x^3, p=(a,b, c,d) *T
grad = 4

A = np.vander(x, grad)
p = np.linalg.solve(A.T@A, A.T@y)
pp = np.polyfit(x, y, 3)
print(p)
print(pp)
print(np.linalg.norm(A@p - y))


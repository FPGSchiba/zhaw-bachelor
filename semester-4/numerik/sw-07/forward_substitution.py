import numpy as np
from backward_substitution import *
def forwardsubst (L, b):
    # Loese L y = b durch Vorwaerts-Einsetzen (L: linke untere Dreiecksmatrix)
    n = len (b)
    y = np. zeros ([n,1])
    bb = np.array(b, np.float64)
    for i in range(n):
        for j in range(i):
            bb [i] = bb[i] - L[i, j] * y[j]
        if L[i,i] == 0:
            raise Exception ( 'L-Matrix ist singulaer!')
        else:
            y[i] = bb[i]/L[i,i]
    return y

if __name__ == '__main__':
    L = np. array([[1, 0, 0], [2, 1, 0], [3, 0, 1]])
    U = np.array ([[1,-2,-1], [0, 3, 3], [0, 0,-2]])
    b = np.array ([[3], [0], [3]] )
    y = forwardsubst(L, b)
    x = backsubst(U, y)
    print( 'Lösung\n', x)
    r = b- (L @ U) @ x
    print('Residuum\n', r)

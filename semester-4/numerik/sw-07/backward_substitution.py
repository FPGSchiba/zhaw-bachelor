import numpy as np

def backsubst(U, y):
    # Berechnet die Loesung x von U x = y durch Rueckwaerts-Einsetzen
    # Dabei ist U eine rechte obere Dreiecksmatrix
    n= len(y)
    x = np.zeros ([n,1])
    yy = np. array (y, np.float64)
    for i in range (n-1, -1, -1):
        for j in range ( i+1, n):
            yy[i] = yy[i] - U[i,j] * x[j]
        if U[i,i] == 0:
            raise Exception('U-Matrix ist singulaer!')
        else:
            x[i] = yy[i]/U[i,i]
    return x

if __name__ == '__main__':
    U = np.array([[1, -2, -1], [0, 3, 31], [0, 0, -2]])
    y = np.array([[3], [-6], [-6]])
    x = backsubst(U, y)
    print( 'Lösung\n', x)
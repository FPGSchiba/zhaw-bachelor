import numpy as np

def LUFaktoren(A):
    # Gauss-Algorithmus zur Berechnung der Dreiecksmatrizen L und U, A=L*U
    # L: linke untere Dreiecksmatrix, U ist rechte obere Dreiecksmatrix
    n=len(A)
    L=np.eye(n)
    U=np.array(A, dtype=np.float64)
    for k in range(n):
        if U[k,k]==0:
            raise Exception('Null-Pivot')
        else:
            L[k+1:n,k] = U[k+1:n,k]/U[k,k]
            for j in range(k+1,n):
                U[j,:] = U[j,:]-L[j,k]*U[k,:]
    return L, U

if __name__ == '__main__':
    A = np.array([[1,-2,-1],[2,-1,1],[3,-6,-5]])
    L, U = LUFaktoren(A)
    print(L)
    print(U)

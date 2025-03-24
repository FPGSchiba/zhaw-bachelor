def bisektion(f, a=1, b=2, tol=1.e-6):
    k = 0 # zaehlt Schleifendurchlaeufe
    
    if f(a)*f(b) > 0:
        print("Bisektion unmoeglich")
        return

    while abs(b-a) > tol:
        mid = (a+b)/2 # Intervallmittelpunkt
        fmid = f( mid )
        k += 1
        # Entscheid ob linkes oder rechtes teilintervall
        if fmid * f(b) < 0:
            a = mid
        elif fmid * f(b)> 0:
            b = mid
        else:
            return mid, mid, k
        print(a, b, k)
    return a, b, k

def f1(x):
    y = x**2 - 3
    return y

def f2(x):
    y = x**3 - 3
    return y

def f3(x):
    return 3 - x**2

a, b, k = bisektion(f3,1, 2)
print(a, b, k)
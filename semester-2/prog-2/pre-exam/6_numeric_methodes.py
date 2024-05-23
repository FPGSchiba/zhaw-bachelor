'''
Aufgabe 6: Numerische Methoden

Gegeben sei ein folgendes Numpy-Array:
  my_array = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

1) Geben Sie die Selektionsoperatoren für folgende Ausgaben an:
  a) Nur die erste Zeile ([1, 2, 3])
  b) Die dritte Spalte ([3, 6, 9])
  c) Die zweite Spalte und die ersten beiden Zeilen ([2, 5])

2) Erstellen Sie ein ein boolesches Array my_boolean_array, bei dem die
  Zelle i,j den Wert 'True' hat, wenn die Zahl in my_array grösser als 5
  ist, sonst 'False'.

3) Schreiben Sie eine Funktion percentarray, welche zu einem zweidimensionalen
  Array ein ebensolches Array zurückliefert, in welchem jedes Feld das 
  Verhältnis vom Ursprungswert zur Ursprungssumme über alle Felder aufweist. 
  Somit muss die Summe über alle Felder des Ergebnisses 1.0 betragen, was mit 
  einem Vergleichsaufruf in Python belegt werden muss.

4) Entwickeln Sie eine Klassendefinition, welche mit einem Array initialisiert 
  wird und anschliessend die in 2) und 3) definierten Funktionalitäten mit 
  einfachen Methodenaufrufen erlaubt.
'''

import numpy as np

my_array = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# 1
## a)
print(f'1 a) {my_array[0]}')
## b)
print(f'1 b) {my_array[:, 2]}')
## c)
print(f'1 c) {my_array[:2, 1]}')

# 2
print(my_array > 5)


# 3
def percentarray(array):
    new_array = array / array.sum()
    if new_array.sum() == 1:
        return new_array
    return None


print(percentarray(my_array))


# 4
class Numpy2D:
    def __init__(self, array):
        self.array = array

    def percentarray(self):
        new_array = array / array.sum()
        if new_array.sum() == 1:
            self.array = new_array
        return self.array

    def greater_than(self, number):
        return self.array > number

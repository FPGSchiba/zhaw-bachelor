# Importiere das Modul für Zufallszahlen
import random as rand
# Generiere eine Zahl zwischen minNumber und maxNumber
minNumber = 1
maxNumber = 8
number2guess = rand.randint( minNumber, maxNumber )
numberguessed = 0
print("Willkommen beim Zahlen raten. Sie müssen eine Zahl zwischen", minNumber, "und", maxNumber, "erraten.")
print()

while numberguessed != number2guess:
    numberguessed = int( input( "Bitte geben Sie ihre Zahl ein: " ))
    if numberguessed < number2guess:
        print( "Die gesuchte Zahl ist höher.")
    elif numberguessed > number2guess:
        print( "Die gesuchte Zahl ist tiefer.")
    else:
        print( "Sehr gut! Sie haben die Zahl gefunden!.")
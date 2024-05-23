"""
Aufgabe 4: Objektmodellierung einer Tier-Taxonomie / 13 Punkte

Ein Zoo hält drei Tiere der Klasse 'Fish'.
- Das Tier 'Stingray' hat 0 Beine, ist ein Räuber, ist für den Menschen giftig.
- Das Tier 'Dogfish' hat 0 Beine, ist ein Räuber, ist für den Menschen harmlos.
- Das Tier 'Haddock' hat 0 Beine, ist kein Räuber, ist für den Menschen harmlos.

Entwickeln Sie die Basisklasse und die drei spezialisierten Klassen jeweils mit 
Konstruktor-Methode. Bestimmen Sie die geeignete Ebene für alle Attribute, so
auch für die beiden booleschen Attribute 'predator' (ist Räuber oder nicht) und 
'venomous' (ist giftig oder nicht). Ist eine Eigenschaft bei allen drei Tieren 
gleich, so soll sie auf Ebene der Basisklasse modelliert sein.
"""


class Animal:
    def __init__(self, name, num_legs=2, predator=False, venomous=False):
        self.num_legs = num_legs
        self.name = name
        self.predator = predator
        self.venomous = venomous


class Fish(Animal):
    def __init__(self, name, predator=False, venomous=False):
        super().__init__(name, 0, predator, venomous)


class Stingray(Fish):
    def __init__(self):
        super().__init__('Stingray', True, True)


class Dogfish(Fish):
    def __init__(self):
        super().__init__('Dogfish', True, False)


class Haddock(Fish):
    def __init__(self):
        super().__init__('Haddock', False, False)

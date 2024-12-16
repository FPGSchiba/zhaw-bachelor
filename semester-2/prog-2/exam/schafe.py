""" 	 	    		
Aufgabe 4: Klassen modellieren mit Tieren (16P)

Ein Bauer hat vier Schafe, welche sich nebst dem Namen in insgesamt drei
Wesensmerkmalen unterscheiden. Er möchte die Tiere, welche in der Datei
schafe.pdf abgebildet sind, programmatisch digitalisieren.

Entwickeln Sie eine geeignete methodenlose Python-Klassendefinition mit
versteckten Attributen für die unterschiedlichen Eigenschaften der Tiere
und einem zweckmässig parametrisierten Konstruktor. Der Tiername soll
nicht als Attribut geführt werden. (5P)

Legen Sie in einem geeignet markierten Hauptprogramm für jedes Schaf
zudem eine Beispielinstanz an, deren Objektnamen die Zuordnung zum
jeweiligen Schaf eindeutig widerspiegelt. (3P)

Ergänzen Sie anschliessend eine Methode, damit Bruno gelegentlich auch
ohne sein Zubehör unterwegs sein kann. Versehen Sie die Methode mit
einer minimalen Dokumentation (Einzeiler) um den Zweck der Methode zu
verstehen. (3P)

Führen Sie schliesslich per Vererbung eine Klasse Leitschaf mit
optimiertem Konstruktor ein. Ein Leitschaf hat immer eine Glocke, aber
auch ein weiteres Merkmal, eine essentielle Altersangabe.
Geben Sie auch hierfür im Hauptprogramm ein Beispiel für Brunos
Schwester Brunhilde. Sie trägt das gleiche Fell wie ihr Bruder, aber
keine Hörner, und wurde zu Weihnachten 2017 geboren. (5P)
"""
import datetime


class Schaf:
    def __init__(self, fellfarbe, horner, glocke):
        self.__fellfarbe = fellfarbe
        self.__horner = horner
        self.__glocke = glocke

    def entferne_zubehoer(self):
        """Entfernt das Zubehör des Schafs."""
        self.__glocke = False


class Leitschaf(Schaf):
    def __init__(self, fellfarbe, horner, alter):
        super().__init__(fellfarbe, horner, True)
        self.__alter = alter


# Hauptprogramm
if __name__ == "__main__":
    schafe = {
        "Flocon": Schaf("Weiss", True, False, ),
        "Lamberto": Schaf("Schwarz", True, False, ),
        "Neige": Schaf("Weiss", False, False),
        "Bruno": Schaf("Weiss", True, True)
    }

    # Beispiel für Brunos Schwester Brunhilde
    Brunhilde = Leitschaf("weiß", False, datetime.date(2017, 12, 24))

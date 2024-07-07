""" 	 	    		
Aufgabe 5: Umgang mit dem Internet (18P)

a) 6P: Vervollständigen Sie die nachfolgende Funktion bis sie funktioniert und eine Antwort liefert.
Die Antwort muss aus einem Geheimwort (Substantiv in beliebig deklinierter Form) bestehen und soll menschenlesbar,
also nicht in Binärform, typisiert sein. Tragen Sie anschliessend das retournierte Geheimwort unten ein. Hinweis:
Die Anfrage wird nur funktionieren, wenn Sie hinter die Portnummer einen Pfad anhängen zusammengesetzt aus dem Wort
"secret" und der Zahl 2519.

Geheimwort: Schwesterschiffe
"""
import requests


def geheimcode():
    url = "http://160.85.252.148:12347/secret2519"
    # HTTP-Anfragen können mit Headerzeilen (Schlüssel-Wert-Paare in 'headers') parametrisiert werden.
    request = requests.get(url, headers={'X-Key': '408'}, timeout=15)
    while request.status_code == 404:
        request = requests.get(url, headers={}, timeout=15)
        print(request.status_code)
    return request.content.decode('utf-8')


print(geheimcode())

"""
b) 6P: Die nachfolgende Funktion soll über das Internet auf Port 1155 bereitgestellt werden.
Unter keinen Umständen darf sie vor der letzten Return-Anweisung unkontrolliert abbrechen.
Identifizieren Sie drei kritische Abbruchpunkte und sichern Sie diese über geeignete Massnahmen direkt am Funktionsanfang ab.
"""


def netzfunktion(g: int, q: str) -> int:
    # Massnahmenbeginn
    if not isinstance(g, int) and not isinstance(g, float):
        return 0
    if g == 0:
        return 0
    if not isinstance(q, str) and not isinstance(q, list):
        return 0
    # Massnahmenende

    g += 1
    z = 42 / g
    if str(z) in q:
        g -= g
    return g


"""
c) 6P: Strukturierte Daten werden oft im portablen JSON-Format über das Internet übertragen.
Sie erhalten nun eine kulinarische Nachricht in eben jenem Format.
Komplettieren Sie die Empfangsfunktion zur Extraktion der menschenlesbaren Nachricht aus den über das Netzwerk empfangenen Daten.
Hinweis: Die Nachricht ist mehrfach kodiert. Probieren Sie allenfalls unterschiedliche Dekodierungen aus.
Weiterer Hinweis: Für eine der Dekodierungen ist eine auf "decode" endende Funktion aus dem Modul "base64" nützlich,
welche Sie allenfalls in der Python-Hilfe nachschlagen müssen.
"""

import json
import base64


def empfang(n: bytes) -> str:
    data = json.loads(n)
    return base64.b64decode(data[0]['text']).decode('utf-8')


print(empfang(b'[{"text": "R2Viw6Rjaw=="}]'))

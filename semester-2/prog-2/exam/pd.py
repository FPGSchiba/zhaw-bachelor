""" 	 	    		
Aufgabe 6: Tabellendaten (13P)

Ein Buchladen hält seine Daten in verkauf.csv, kunden.csv, buchliste.csv und preise.csv.
Von besonderem Interesse ist die dritte Datei. Ein kleiner Ausschnitt, die Datei ist viel länger:
    
Autor,Titel,Erscheinungsjahr
Austin;Jane, Stolz und Vorurteil, 1813
Dickens;Charles, A Tale of two Cities, 1859
Dickens;Charles, Great Expectations, 1861
"""
import pandas as pd
import matplotlib.pyplot as plt

"""
1) 3P: Lesen Sie die relevante Datei mit Pandas ein und erstellen Sie eine geeignete Datenstruktur.
Verwenden Sie diese Struktur für die nächsten Teilaufgaben.
"""
verkauf = pd.read_csv('verkauf.csv')
kunden = pd.read_csv('kunden.csv')
buchliste = pd.read_csv('buchliste.csv')
preise = pd.read_csv('preise.csv')

"""
2) 1P: Welche Bücher des Autors "Charles Dickens" finden sich in der Liste? Geben Sie diese auf der Konsole aus.
"""
print(buchliste.query('Autor = Dickens;Charles'))

"""
3) 2P: Welche Bücher der Autorin "Jane Austin" sind nach 1800 erschienen? Geben Sie diese auf der Konsole aus.
"""
print(buchliste.query('Autor = Austin;Jane and Erscheinungsjahr > 1800'))

"""
4) 1P: Wie viele unterschiedliche Autoren sind in der Tabelle enthalten? Geben Sie diese auf der Konsole aus.
""" 
print(buchliste['Autor'].unique())

"""
5) 3P: Generieren Sie einen Barplot, bei dem in der X-Achse das Erscheinungsjahr und in der Y-Achse die Anzahl der Bücher,
die in diesem Jahr erschienen sind, angezeigt werden. Die Lösung sollte eine Anzahl an Zeilen aufweisen, die um eins
geringer als die Zahl der erzielbaren Punkte in dieser Teilaufgabe ist.
"""
# Erscheinungsjahr gruppieren und die Anzahl der Bücher pro Jahr zählen
jahr_counts = buchliste['Erscheinungsjahr'].value_counts().sort_index()

# Barplot erstellen
plt.figure(figsize=(10, 6))
jahr_counts.plot(kind='bar', color='skyblue')
plt.title('Anzahl der Bücher pro Erscheinungsjahr')
plt.xlabel('Erscheinungsjahr')
plt.ylabel('Anzahl der Bücher')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

"""
6) 3P: Übersetzen Sie automatisiert den Titel der personenreferenzierenden Spalte, indem Sie deren deutschsprachigen
Titel durch einen anderssprachigen ersetzen. Konsultieren Sie hierfür die Methode rename der Buchdatenstruktur nach
dem Schema rename(..., axis="columns"). Nehmen Sie weiterhin an, eine geeignete und verpflichtend zu nutzende
Übersetzungsdatei words.csv mit folgendem Format vorliegen zu haben.

dt|en
Apfel|apple
Autor|author
"""

translations = pd.read_csv('words.csv', sep='|', names=['de', 'en'], header=None)

translation_dict = dict(zip(translations['de'], translations['en']))
buchliste.rename(columns=translation_dict, inplace=True, axis="columns")

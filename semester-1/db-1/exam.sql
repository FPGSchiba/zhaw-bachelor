CREATE TABLE Personen (
    PNr int PRIMARY KEY,
    Vorname varchar(50),
    Name varchar(50),
    Geschlecht varchar(1),
    Jahrgang int
);

CREATE TABLE Module (
    Bezeichnung varchar(50) PRIMARY KEY
);

CREATE TABLE  Dozenten (
    PNr int PRIMARY KEY REFERENCES Personen,
    Lohnstufe int NOT NULL
);

CREATE TABLE Teilnehmer (
    PNr int PRIMARY KEY REFERENCES Personen
);

CREATE TABLE Zuordnung (
    DozPNr int REFERENCES Dozenten,
    Bezeichnung varchar(50) REFERENCES Module,
    TeilnPNr int REFERENCES Teilnehmer,
    PRIMARY KEY (TeilnPNr, Bezeichnung)
);

SELECT Name, Bezeichnung, count(TeilnPNr) as count_teiln FROM
    (Zuordnung JOIN Module M on M.Bezeichnung = Zuordnung.Bezeichnung)
    JOIN Personen p ON DozPNr = p.PNr
GROUP BY Bezeichnung
ORDER BY count_teiln;

SELECT Vorname, Name FROM
    Zuordnung z JOIN Personen p ON z.TeilnPNr = p.PNr
WHERE Bezeichnung = ('Quantum Computing' OR Bezeichnung = 'Data Science') AND Bezeichnung != 'Databases';

SELECT Name FROM
        (SELECT Bezeichnung, count(TeilnPNr) as count_teiln, DozPNr FROM Zuordnung GROUP BY Bezeichnung)
            JOIN Personen p ON DozPnr = p.PNr
WHERE (Bezeichnung LIKE '%Data%' or Bezeichnung LIKE '%data%') and count_teiln > 3;
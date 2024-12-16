import math

documents = ["Beim Fussball dauert ein Spiel neunzig Minuten",
             "Beim Fussball muss das Runde (der Ball) in das Eckige (das Tor)",
             "Nie war ein Tor so wertvoll wie jetzt, Fussball ist ein einzigartiger Sport",
             "Tor, Tor, Tor, das Finale der Weltmeisterschaft ist entschieden",
             "Im Sport ist kein Moment wie der andere", "Mit Sport hälst du dich fit"]


def tf(term, doc):
    doc = documents[doc].split(" ")
    return sum([1 for t in doc if t == term]) / len(doc)


def idf(term):
    count = 0
    for document in documents:
        doc = document.split(" ")
        if term in doc:
            count += 1
    if count != 0:
        return math.log(len(documents) / count)
    return 0


def tfidf(term, doc):
    return tf(term, doc) * idf(term)


if __name__ == '__main__':
    for i in range(len(documents)):
        print(f"DOC-{i + 1} (Fussball): {tfidf('Fussball', i)}")
        print(f"DOC-{i + 1} (Tor): {tfidf('Tor', i)}")
        print(f"DOC-{i + 1} (Sport): {tfidf('Sport', i)}")

""" 	 	    		
Aufgabe 3: Sortieren und Komplexität (11P)

- Aufgabenstellung siehe Blatt Teil 2

Antwort zu a): 1 (Also, dass das Array mit einem Random mischen sortiert ist)

Antwort zu b): undendlich (Es kann sein, dass Sunny-Sort nie eine Lösung findet.)

Antwort/Code zu c):
"""

# Code in sort + mix ergänzen. Die Methode check ist bereits vollständig.
# WICHTIG: Die Lösung wird auch gewertet, wenn die Umsetzung nicht rekursiv erfolgt.

import random


class SunnySort:
    def sort(self, array):
        """
        array: list of int
        Returns: array sorted in descending order
        Uses ''SunnySort'' as sorting algoritthm
        """
        # l is dividable by 4 by definition
        split_first, split_second = self.split_n_mix(array)
        split_one, split_two = self.split_n_mix(split_first)
        split_three, split_four = self.split_n_mix(split_second)
        split_middle = self.mix([*split_two, *split_three])
        final_array = [*split_one, *split_middle, *split_four]
        if self.check(final_array):
            return final_array
        return self.sort(final_array)

    def split_n_mix(self, array):
        """
        array: list of int
        Returns: splitted and mixed arrays in equal parts
        """
        if len(array) > 2:
            split = int(len(array) // 2)
            split_one = self.mix(array[:split])
            split_two = self.mix(array[split:])
        else:
            split_one = self.mix([array[0]])
            split_two = self.mix([array[1]])
        return split_one, split_two

    def mix(self, array):
        """
        array: list of int
        Returns: a randomly shuffled version of array
        """
        random.shuffle(array)
        return array

    def check(self, array):
        """
        array: list of int
        Returns: True if arrray is sorted in descending order, False otherwise
        """
        # Already completed
        for index in range(len(array) - 1):
            if not (array[index] > array[index + 1]): return False
        return True


# test code

s = SunnySort()
a = [7, 6, 5, 4]
b = [2, 3, 7, 1]

print("a: ", s.check(a))
print("b: ", s.check(b))
print("m: ", s.mix(a))
print("m: ", s.mix(b))
print("s: ", s.sort(a))
print("s: ", s.sort(b))

"""
Antwort zu d): Nein, da es die Vorherigen versuche vergisst und nicht effizient eine Lösung sucht.

Antwort zu e): A wird sich nicht verändern, da der Glücksfaktor bleibt, aber b wird sich ändern, dass 8+n! geschwindigkeit.
"""

""" 	 	    		
Aufgabe 2: Passwortprüfung (10P)

- Aufgabenstellung siehe Blatt Teil 2
"""
import re
import string


def check_password(password: str):
    pass_ok = True
    if len(password) < 7:
        print('Len failed')
        pass_ok = False
    if len(list(set(password))) != len(password):
        print('Dupl failed')
        pass_ok = False

    num_categories_ok = 0
    for char in password:
        if char.isupper():
            num_categories_ok += 1
            break
    for char in password:
        if char.islower():
            num_categories_ok += 1
            break
    for char in password:
        if char.isnumeric():
            num_categories_ok += 1
            break
    for char in password:
        if char in string.punctuation:
            num_categories_ok += 1
            break
    if num_categories_ok < 3:
        print('Cat failed')
        pass_ok = False

    return pass_ok


if __name__ == '__main__':
    print(check_password('Password1'))
    print(check_password('Sp3cia!'))
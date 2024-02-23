# -*- coding: utf-8 -*-
"""
PROG2 V01: Prime Number finder

@date: 22.02.2024
@author: Jann Erhardt
"""
import math

SMALL_PRIME = [2, 3]


def find_prime_numbers(number: int):
    list_of_numbers = [i for i in range(1, number + 1)]
    list_of_check_numbers = [i for i in range(1, math.ceil(math.sqrt(number)) + 1) if i != 1]
    list_of_prime_numbers = list_of_numbers[1:]
    for i, num in enumerate(list_of_numbers):
        for check in list_of_check_numbers:
            print(f'Checking {num} with {check}')
            if num % check == 0 and num != check and num not in SMALL_PRIME:
                if num in list_of_prime_numbers:
                    list_of_prime_numbers.remove(num)
    return list_of_prime_numbers

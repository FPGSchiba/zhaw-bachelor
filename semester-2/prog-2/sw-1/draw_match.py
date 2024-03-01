# -*- coding: utf-8 -*-
"""
PROG2 P01.1: Draw a Match game done with Python

@date: 24.02.2024
@author: Jann Erhardt, Johannes Werder, Simone Fabio
"""
import random

running = True
stack_size = random.randint(20, 200)
players_turn = True if random.randint(0, 1) == 1 else False
num_matches = random.randint(10, stack_size)


def build_bot_moves():
    count = 1
    bot_moves = {}
    for i in range(1, stack_size + 1):
        if count == 1:
            bot_moves[i] = random.randint(1, 3)
            count += 1
        elif count == 4:
            bot_moves[i] = count - 1
            count = 1
        else:
            bot_moves[i] = count - 1
            count += 1
    return bot_moves


def to_roman_numeral(num):
    lookup = [
        (1000, 'M'),
        (900, 'CM'),
        (500, 'D'),
        (400, 'CD'),
        (100, 'C'),
        (90, 'XC'),
        (50, 'L'),
        (40, 'XL'),
        (10, 'X'),
        (9, 'IX'),
        (5, 'V'),
        (4, 'IV'),
        (1, 'I'),
    ]
    res = ''
    for (n, roman) in lookup:
        (d, num) = divmod(num, n)
        res += roman * d
    return res


def show_matches():
    print('=== Macthes ===')
    print(f'Num Matches: {to_roman_numeral(num_matches)}')


def get_max_pullable_matches():
    if num_matches >= 3:
        return 3
    return num_matches


def get_player_input():
    player_input = 0
    max_pullable_matches = get_max_pullable_matches()
    while not (1 <= player_input <= max_pullable_matches):
        try:
            player_input = int(input('Enter a number between 1 and 3: '))
        except ValueError:
            continue
    return player_input


def get_bot_input():
    bot_moves = build_bot_moves()
    return bot_moves[num_matches]


while running:
    show_matches()
    # Player Turn
    if players_turn:
        player_input = get_player_input()
        num_matches = num_matches - player_input
    # AI Turn
    else:
        bot_input = get_bot_input()
        print(f'Bot Pulls: {bot_input}')
        num_matches = num_matches - bot_input
    # Game End Condition
    if num_matches <= 1:
        print('=== Game Ended ===')
        running = False
        if players_turn:
            print('= You Won =')
        else:
            print('= You Lost =')
        print('== GG ==')
    players_turn = not players_turn

import random
import time
import subprocess

import pygame
from button import Button

# Source https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life

SIZE = 300
BEGINNING_CELLS = round((SIZE * SIZE) / 20)
SCALE = 3

FPS = 10

DEAD_CELL = 0
ALIVE_CELL = 1

DEAD_COLOR = pygame.Color(255, 255, 255)
ALIVE_COLOR = pygame.Color(0, 0, 0)

playing = True

environment = [[DEAD_CELL for _ in range(SIZE)] for _ in range(SIZE)]

pygame.init()
screen = pygame.display.set_mode((SIZE * SCALE, SIZE * SCALE))
clock = pygame.time.Clock()


def get_num_neighbors(x, y):
    neighbors = 0
    # Check for errors
    env_size = SIZE - 1
    if x < env_size and environment[y][x + 1] != DEAD_CELL:
        neighbors += 1
    if x > 0 and environment[y][x - 1] != DEAD_CELL:
        neighbors += 1
    if y < env_size and environment[y + 1][x] != DEAD_CELL:
        neighbors += 1
    if y > 0 and environment[y - 1][x] != DEAD_CELL:
        neighbors += 1
    if x < env_size and y < env_size and environment[y + 1][x + 1] != DEAD_CELL:
        neighbors += 1
    if x > 0 and y < env_size and environment[y + 1][x - 1] != DEAD_CELL:
        neighbors += 1
    if y > 0 and x < env_size and environment[y - 1][x + 1] != DEAD_CELL:
        neighbors += 1
    if y > 0 and x > 0 and environment[y - 1][x - 1] != DEAD_CELL:
        neighbors += 1
    return neighbors


def draw_cell(x, y, cell):  # X = 1 -> Scaled-X: 4
    scaled_x = x * SCALE
    scaled_y = y * SCALE
    pos = (scaled_x, scaled_y)
    color = DEAD_COLOR if cell == DEAD_CELL else ALIVE_COLOR
    screen.fill(color, (pos, (SCALE, SCALE)))


def prepare_game():
    global environment
    environment = [[DEAD_CELL for _ in range(SIZE)] for _ in range(SIZE)]
    generated_cells = 0

    for _ in range(BEGINNING_CELLS):
        generating = True
        while generating:
            x = random.randint(0, SIZE - 1)
            y = random.randint(0, SIZE - 1)
            if environment[y][x] == DEAD_CELL:
                environment[y][x] = ALIVE_CELL
                generated_cells += 1
                generating = False

    print(f'Starting Game with: {generated_cells} cells.')
    screen.fill((255, 255, 255), ((0, 0), (SIZE, SIZE)))
    pygame.display.flip()


restart_btton = Button(0,0, 100, 40, screen, 'Restart', prepare_game)
prepare_game()

while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
    # Copy each row so updates don't affect neighbor counts of this generation
    new_environment = [row[:] for row in environment]

    for y, row in enumerate(environment):
        for x, cell in enumerate(row):
            draw_cell(x, y, cell)
            num_neighbors = get_num_neighbors(x, y)
            if cell == DEAD_CELL and num_neighbors == 3:
                new_environment[y][x] = ALIVE_CELL
            elif cell != DEAD_CELL and num_neighbors not in (2, 3):
                new_environment[y][x] = DEAD_CELL

    environment = new_environment
    restart_btton.process()
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

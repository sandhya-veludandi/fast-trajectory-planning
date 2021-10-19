import pygame
import random
import numpy as np

#proportions of pygame screen on computer in pixels
WIDTH, HEIGHT = 505, 505
CELL_SIZE = 5
ROWS, COLUMNS = int(HEIGHT / CELL_SIZE), int(WIDTH / CELL_SIZE)

# grid RGB colors & meanings
BLACK = (0, 0, 0) # grid == 0
WHITE = (255, 255, 255) # grid == 1
GREEN = (50,205,50) # grid == 2
RED = (255,99,71) # grid == 3
GRAY = (211,211,211) # for background
BLUE = (153,255,255) # grid[x][y] == 4, where current position is

#Defining ONE grid (put inside for loop later)
grid = np.zeros((ROWS, COLUMNS))

#green is 2 (start)
grid[0, 0] = 2
#red is 3 (end)
grid[-1, -1] = 3

#Initializing pygame screen
pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Generator")
CLOCK = pygame.time.Clock()
FPS = 30



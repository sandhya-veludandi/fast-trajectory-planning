import random
import pygame
import numpy as np

# Python 3 program of the above approach
ROW = 101
COL = 101

#proportions of pygame screen on computer in pixels
WIDTH, HEIGHT = 505, 505
CELL_SIZE = 5
ROWS, COLUMNS = int(HEIGHT / CELL_SIZE), int(WIDTH / CELL_SIZE)

 #Initializing pygame screen
pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Generator")
CLOCK = pygame.time.Clock()
FPS = 30

# Initialize direction vectors
dRow = [0, 1, 0, -1]
dCol = [-1, 0, 1, 0]
vis = [[False for i in range(101)] for j in range(101)]
cols = 101
rows = 101
grid = [[1 for i in range(cols)] for j in range(rows)] #iterates all as open

# Function to check if mat[row][col]
# is unvisited and lies within the
# boundary of the given matrix
def isValid(row, col):
    global ROW
    global COL
    global vis
     
    # If cell is out of bounds
    if (row < 0 or col < 0 or row >= ROW or col >= COL):
        return False
 
    # If the cell is already visited
    if (vis[row][col]):
        return False
 
    # Otherwise, it can be visited
    return True
 
# Function to perform DFS
# Traversal on the matrix grid[]
def DFS(row, col, grid):
    global dRow
    global dCol
    global vis
     
    # Initialize a stack of pairs and
    # push the starting cell into it
    st = []
    st.append([row, col])
 
    # Iterate until the
    # stack is not empty
    while (len(st) > 0):
        # Pop the top pair
        curr = st[len(st) - 1]
        st.remove(st[len(st) - 1])
        row = curr[0]
        col = curr[1]
 
        # Check if the current popped
        # cell is a valid cell or not
        if (isValid(row, col) == False):
            continue
 
        # Mark the current
        # cell as visited
        vis[row][col] = True
 
        # Print the element at
        # the current top cell
        # Check probability
        rand = random.random()

        # if < 0.3 then close the site
        if(rand >= 0.3):
            grid[row][col] = 0
 
        # Push all the adjacent cells
        for i in range(4):
            adjx = row + dRow[i]
            adjy = col + dCol[i]
            st.append([adjx, adjy])
 
def drawGrid():
    # Function call
    DFS(0, 0, grid)

    # grid RGB colors & meanings
    WHITE = (255, 255, 255) # grid == 1
    BLACK = (0, 0, 0) # grid == 0
    GREEN = (50,205,50) # grid == 2
    RED = (255,99,71) # grid == 3
    GRAY = (211,211,211) # for background
    BLUE = (153,255,255) # grid[x][y] == 4, where current position is
    idx_to_color = [WHITE, BLACK, GREEN, RED, BLUE]

    # set the height/width of each location on the grid
    height = 4
    width = height # i want the grid square
    margin = 1 # sets margin between grid locations

    grid[0][0] = 2
    grid[100][100] = 3

    SCREEN.fill(GRAY) # fill background in grey
     
    for i in range(101):
        for j in range(101):
            COLOR = idx_to_color[grid[i][j]]
            pygame.draw.rect(SCREEN, COLOR, 
                [(margin + width) * j + margin, 
                (margin + height) * i + margin,
                width, height])
    # update screen
    pygame.display.update()

if __name__ == '__main__':
    running = True
    while running:
        CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        drawGrid()

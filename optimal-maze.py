import sys
import random
from pathlib import Path
import pygame

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
# Function to check if mat[row][col] is unvisited and lies within the boundary of the given matrix
def isValid(row, col):
    global vis

    # If cell is out of bounds
    if (row < 0 or col < 0 or row >= 101 or col >= 101):
        return False
 
    # If the cell is already visited
    if (vis[row][col]):
        return False
 
    # Otherwise, it can be visited
    return True
 
# generates random grid using DFS
def DFS(row, col, grid):
    global dRow
    global dCol
    global vis

    # Initialize a stack of pairs and push the starting cell into it
    st = []
    st.append([row, col])

    # Iterate until the stack is not empty
    while (len(st) > 0):
        # Pop the top pair
        curr = st[len(st) - 1]
        st.remove(st[len(st) - 1])
        row = curr[0]
        col = curr[1]

        # Check if the current popped cell is a valid cell or not
        if (isValid(row, col) == False):
            continue

        # Mark the current cell as visited
        vis[row][col] = True

        # Print the element at the current top cell
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

class Node:
    # Initialize the class
    def __init__(self, position, parent):
        self.position = position
        self.parent = parent
        self.g = 0 # Distance to start node
        self.h = 0 # Distance to goal node
        self.f = 0 # Total cost
    # Compare nodes
    def __eq__(self, other):
        return self.position == other.position
    # Sort nodes
    def __lt__(self, other):
         return self.f < other.f
    # Print node
    def __repr__(self):
        return ('({0},{1})'.format(self.position, self.f))


# a star
def asearch(grid, start, end):
    open = []
    closed = []
    start_node = Node(start, None)
    goal_node = Node(end, None)
    open.append(start_node)
    while len(open) > 0:
        open.sort() #get lowest cost
        current_node = open.pop(0)
        # print(current_node)
        closed.append(current_node)
        if current_node == goal_node:
            path = []
            while current_node != start_node:
                path.append(current_node.position)
                grid[current_node.position[0]][current_node.position[1]] = 4
                current_node = current_node.parent
            # Return reversed path
            return path[::-1]
        
        (x, y) = current_node.position
        # Get neighbors
        neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        for next in neighbors:
            if((0 <= next[0] < 101) & (0 <= next[1] < 101)):
                map_value = grid[next[0]][next[1]]
            else:
                continue
            # Get value from map
            #map_value = grid[next[0]][next[1]]
            # Check if the node is a wall
            if(map_value == 1):
                continue
            # Create a neighbor node
            neighbor = Node(next, current_node)
            # Check if the neighbor is in the closed list
            if(neighbor in closed):
                continue
            # Generate heuristics (Manhattan distance)
            neighbor.g = abs(neighbor.position[0] - start_node.position[0]) + abs(neighbor.position[1] - start_node.position[1])
            neighbor.h = abs(neighbor.position[0] - goal_node.position[0]) + abs(neighbor.position[1] - goal_node.position[1])
            neighbor.f = neighbor.g + neighbor.h
            # Check if neighbor is in open list and if it has a lower f value
            if(add_to_open(open, neighbor) == True):
                # Everything is green, add neighbor to open list
                open.append(neighbor)    
    
    return "I cannot reach the target"

def add_to_open(open, neighbor):
    for node in open:
        if (neighbor == node and neighbor.f >= node.f):
            return False
    return True

def create_grid_solution(grid_arg):
    grid = [[1 for i in range(cols)] for j in range(rows)]
    # create the randomly generated grid
    if len(grid_arg) < 1: DFS(0, 0, grid)
    # use testcase grid
    else: grid = grid_arg 

    grid[0][0] = 2
    grid[100][100] = 3

    start = (0,0)
    end = (100,100)

    print("TESTCASE ************************************")
    print(grid)

    path = asearch(grid, start, end)

    print("RESULT ***************************************")
    print(grid)
    drawGrid(grid)
 
def drawGrid(grid):
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
    SCREEN.fill(GRAY) # fill background in grey
    
    # mark start and ending positions in green and red
    grid[0][0] = 2
    grid[100][100] = 3
    # print(path)
    #draw_grid(map, 101, 101, spacing=1, path=path, start=start, goal=end)
    # print('Steps to goal: {0}'.format(len(path)))
    for i in range(101):
        for j in range(101):
            COLOR = idx_to_color[grid[i][j]]
            pygame.draw.rect(SCREEN, COLOR, 
                [(margin + width) * j + margin, 
                (margin + height) * i + margin,
                width, height])
    # update screen
    pygame.display.update()

def convert(grid_arg):
    input = grid_arg[1:-1]
    # print(grid_arg)
    grid_result = []
    sub_array = []
    for char in input:
        if char == '[':
            sub_array = []
        if char.isdigit(): 
            sub_array.append(int(char))
        if char == ']': 
            # print(sub_array)
            grid_result.append(sub_array)

    # print(grid_result)
    return grid_result

#driver code
if __name__ == '__main__':
    num_of_args = len(sys.argv)
    grid_arg = []
    drawGridYet = False
    if num_of_args > 1:
        grid_arg = Path(sys.argv[1]).read_text()
        grid_arg = grid_arg.replace('\n', '')
        saved_grid_string = grid_arg
        grid_arg = convert(grid_arg)
        # print(grid_arg)
        #if drawing grid testcase solution
        if saved_grid_string.__contains__("4"):
            drawGrid(grid_arg)
            drawGridYet = True
            
    #if random or testcase grid run create_grid_solution 
    if not(drawGridYet): create_grid_solution(grid_arg)
 
    running = True
    while running:
        CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
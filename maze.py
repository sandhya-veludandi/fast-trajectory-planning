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
 
# Function to perform DFS
# Traversal on the matrix grid[]
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

class heap:
    def __init__(self):
        self.heapList = [0]
        self.currentSize = 0
    
    def percUp(self,i):
        while i // 2 > 0:
            if self.heapList[i].h < self.heapList[i // 2].h:
                tmp = self.heapList[i // 2]
                self.heapList[i // 2] = self.heapList[i]
                self.heapList[i] = tmp
            i = i // 2

    def insert(self,k):
        self.heapList.append(k)
        self.currentSize = self.currentSize + 1
        self.percUp(self.currentSize)
    
    def percDown(self,i):
        while (i * 2) <= self.currentSize:
            if(isinstance(self.heapList[i], int)):
                mc = self.minChild(i)
                i = mc
                continue
            mc = self.minChild(i)
            if self.heapList[i].h > self.heapList[mc].h:
                tmp = self.heapList[i]
                self.heapList[i] = self.heapList[mc]
                self.heapList[mc] = tmp
            i = mc

    def minChild(self,i):
        if i * 2 + 1 > self.currentSize:
            return i * 2
        else:
            if self.heapList[i*2].h < self.heapList[i*2+1].h:
                return i * 2
            else:
                return i * 2 + 1
    
    def delMin(self):
        retval = self.heapList[1]
        self.heapList[1] = self.heapList[self.currentSize]
        self.currentSize = self.currentSize - 1
        self.heapList.pop()
        self.percDown(1)
        return retval

    def buildHeap(self,alist):
        i = len(alist) // 2
        self.currentSize = len(alist)
        self.heapList = [0] + alist[:]
        while (i > 0):
            self.percDown(i)
            i = i - 1

class Node:
    # Initialize the class
    def __init__(self, position, parent):
        self.position = position
        self.parent = parent
        self.g = 0 # Goal distance of state s
        self.h = 0 # Goal s - state s
        self.f = 0 # Total cost
    # Compare nodes
    def __eq__(self, other):
        if(isinstance(other, int)):
            return False
        return self.position == other.position
    # Sort nodes
    def __lt__(self, other):
        if(isinstance(other, int)):
            return False
        return self.f < other.f
    # Print node
    def __repr__(self):
        return ('({0},{1})'.format(self.position, self.f))

# a star forward
def adaptiveA(grid, start, end):
    closed = []

    open = heap()

    start_node = Node(start, None)
    goal_node = Node(end, None)

    open.insert(start_node)

    while open.currentSize > 0:
        # open.buildHeap(open.heapList)
        current_node = open.delMin() #gets the minimum and deletes it from the heap
        while(current_node == 0):
            current_node = open.delMin() #deletes min again because heap is automatically created with 0
            # print(current_node.h)
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
            # Check if the node is a wall
            if(map_value == 1):
                continue

            grid[next[0]][next[1]] = 5
            # Create a neighbor node
            neighbor = Node(next, current_node)
            # Check if the neighbor is in the closed list
            if(neighbor in closed):
                continue
            goal =  goal_node.position[0] + goal_node.position[1]
            # h = abs(neighbor.position[0] - goal_node.position[0]) + abs(neighbor.position[1] - goal_node.position[1])
            neighbor.g = (abs(neighbor.position[0] - start_node.position[0]) + abs(neighbor.position[1] - start_node.position[1]))
            neighbor.h = goal - (abs(neighbor.position[0] - start_node.position[0]) + abs(neighbor.position[1] - start_node.position[1]))
            neighbor.f = neighbor.g + neighbor.h
            # Check if neighbor is in open list and if it has a lower f value
            if(add_to_open(open, neighbor) == True):
                # Everything is green, add neighbor to open list
                open.insert(neighbor)    
    
    return []

# backwardA
def backwardA(grid, start, end):
    closed = []

    open = heap()

    start_node = Node(start, None)
    goal_node = Node(end, None)

    open.insert(start_node)

    while open.currentSize > 0:
        current_node = open.delMin() #gets the minimum and deletes it from the heap
        while(current_node == 0):
            current_node = open.delMin() #deletes min again because heap is automatically created with 0

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
        neighbors = [(x+1, y), (x, y+1), (x-1, y), (x, y-1)]

        for next in neighbors:
            if((0 <= next[0] < 101) & (0 <= next[1] < 101)):
                map_value = grid[next[0]][next[1]]
            else:
                continue
            # Get value from map
            # Check if the node is a wall
            if(map_value == 1):
                continue
            # Colors neighbors gray to represent that we've expanded it
            grid[next[0]][next[1]] = 5
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
            if(add_to_openS(open, neighbor) == True):
                # Everything is green, add neighbor to open list
                open.insert(neighbor) 
    return []

# forwardA_lagestG
def forwardA_largestG(grid, start, end, close, opened):
    closed = []

    open = heap()

    start_node = Node(start, None)
    goal_node = Node(end, None)

    open.insert(start_node)

    while open.currentSize > 0:
        # open.buildHeap(open.heapList)
        current_node = open.delMin() #gets the minimum and deletes it from the heap
        while(current_node == 0):
            current_node = open.delMin() #deletes min again because heap is automatically created with 0

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
            # Check if the node is a wall
            if(map_value == 1):
                #grid[next[0]][next[1]] = 6 # Represents wall seen
                continue
            # Colors neighbors gray to represent that we've expanded it
            grid[next[0]][next[1]] = 5
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
                open.insert(neighbor) 
    return []

# forwardA_smallestG
def forwardA_smallestG(grid, start, end):
    closed = []

    open = heap()

    start_node = Node(start, None)
    goal_node = Node(end, None)

    open.insert(start_node)

    while open.currentSize > 0:
        # open.buildHeap(open.heapList)
        current_node = open.delMin() #gets the minimum and deletes it from the heap
        while(current_node == 0):
            current_node = open.delMin() #deletes min again because heap is automatically created with 0

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
            # Check if the node is a wall
            if(map_value == 1):
                continue
            # Colors neighbors gray to represent that we've expanded it
            grid[next[0]][next[1]] = 5
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
            if(add_to_openS(open, neighbor) == True):
                # Everything is green, add neighbor to open list
                open.insert(neighbor) 
    return []

def add_to_open(open, neighbor):
    for node in open.heapList:
<<<<<<< HEAD
        if (neighbor == node and neighbor.f > node.f):
            return False
        
=======
        if (neighbor == node):
            if(neighbor.g >= node.g):
                return False
>>>>>>> refs/remotes/origin/main
    return True

def add_to_openS(open, neighbor):
    for node in open.heapList:
        if (neighbor == node):
            if(neighbor.g <= node.g):
                return False
    return True

def create_grid_solution(search_type, grid_arg):
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
    # print(grid)

    if search_type == 1: 
        path = adaptiveA(grid, start, end) 
    elif search_type == 2: 
        path = backwardA(grid, start, end)
    elif search_type == 3: 
        close = []
        open = heap()
        path = forwardA_largestG(grid, start, end, close, open)
    elif search_type == 4: 
        path = forwardA_smallestG(grid, start, end)
    

    print("RESULT ***************************************")
    # print(grid)
    drawGrid(grid, search_type)

def drawGrid(grid, search_type):
    # grid RGB colors & meanings
    WHITE = (255, 255, 255) # grid == 1
    BLACK = (0, 0, 0) # grid == 0
    GREEN = (50,205,50) # grid == 2
    RED = (255,99,71) # grid == 3
    GRAY = (211,211,211) # for background
    BLUE = (153,255,255) # grid[x][y] == 4, where current position is
    idx_to_color = [WHITE, BLACK, GREEN, RED, BLUE, GRAY]
    #idx_to_color = [GRAY, GRAY, GREEN, RED, BLUE, WHITE, BLACK]
    # set the height/width of each location on the grid
    height = 4
    width = height # i want the grid square
    margin = 1 # sets margin between grid locations
    SCREEN.fill(GRAY) # fill background in grey

    # mark start and ending positions in green and red
    grid[0][0] = 2
    grid[100][100] = 3

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

if __name__ == '__main__':
    num_of_args = len(sys.argv)
    grid_arg = []
    if num_of_args < 2: 
        print("Please enter 1, 2, 3, or 4 for adaptive, backward, forward largest g, or forward smallest g searches")
        exit(1)
    if num_of_args > 2:
        grid_arg = Path(sys.argv[2]).read_text()
        grid_arg = grid_arg.replace('\n', '')
        grid_arg = convert(grid_arg)
        # print(grid_arg)
    #if random or testcase grid run create_grid_solution 
    create_grid_solution(int(sys.argv[1]), grid_arg)
 
    running = True
    while running:
        CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
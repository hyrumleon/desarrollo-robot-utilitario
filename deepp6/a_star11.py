#a_star11.py 

import math

class Node:
    def __init__(self, grid, x, y):
        self.x = x
        self.y = y
        self.grid = grid
        self.type = 'road'
        self.g_score = float('inf')
        self.f_score = float('inf')

    def get_neighbors(self):
        # Collection of arrays representing the x and y displacement
        rows = len(self.grid)
        cols = len(self.grid[0])
        directions = [[1, 0], [1, 1], [0, 1], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]
        neighbors = []
        for direction in directions:
            neighbor_x = self.x + direction[0]
            neighbor_y = self.y + direction[1]
            if 0 <= neighbor_x < cols and 0 <= neighbor_y < rows:
                neighbors.append(self.grid[neighbor_y][neighbor_x])
        return neighbors


rows = 40
cols = 40
grid = []

file = open(r'C:\Users\leonl\Downloads\arauco2\DEEPp5\deepp6\a_star.in', 'r')

lines = file.read().split('\n')
file.close()

start = None
end = None

# set test data
for i in range(rows):
    row = list(map(int, lines[i].split()))
    row_nodes = []
    for j in range(len(row)):
        node = Node(grid, j, i)
        element = row[j]
        if element == 1:
            node.type = 'wall'
        elif element == 2:
            if not start:
                start = node
            elif not end:
                end = node

        row_nodes.append(node)
    grid.append(row_nodes)

# g score, estimated distance

# returns distance between two nodes
def distance(node1, node2):
    return math.sqrt((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2)

# Measures distance from node to endpoint with nodes only being able to travel vertically, horizontally, or diagonally
def h_score(start, end):
    x_dist = abs(end.x - start.x)
    y_dist = abs(end.y - start.y)
    diagonal_steps = min(x_dist, y_dist)
    straight_steps = y_dist + x_dist - 2 * diagonal_steps
    return diagonal_steps * math.sqrt(2) + straight_steps

def reconstruct_path(grid, came_from, current):
    path = [current]
    current_key = str(current.x) + ' ' + str(current.y)
    while current_key in came_from:
        current = came_from[current_key]
        current_key = str(current.x) + ' ' + str(current.y)
        path.insert(0, current)
    return path

# Performs the pathfinding algorithm. start are end are (x, y) tuples
def a_star(grid, start, end):
    open_set = []
    closed_set = []
    came_from = {}

    start.g_score = 0
    start.f_score = h_score(start, end)

    open_set.append(start)

    while open_set:
        current = lowest_f_score(open_set)
        open_set.remove(current)
        closed_set.append(current)

        if current == end:
            return reconstruct_path(grid, came_from, current)

        for neighbor in current.get_neighbors():
            if neighbor in closed_set:
                continue

            # Calculating the weight of moving to a wall or an empty space
            tentative_g_score = current.g_score + calculate_weight(current, neighbor)

            if neighbor not in open_set:
                open_set.append(neighbor)
            elif tentative_g_score >= neighbor.g_score:
                continue  # Not a better path

            came_from[str(neighbor.x) + ' ' + str(neighbor.y)] = current
            neighbor.g_score = tentative_g_score
            neighbor.f_score = neighbor.g_score + h_score(neighbor, end)

# Calculate the weight for each move
def calculate_weight(current, neighbor):
    if neighbor.type == 'wall':
        # If diagonal movement, weight is multiplied by 30 * sqrt(2)
        if abs(current.x - neighbor.x) == 1 and abs(current.y - neighbor.y) == 1:
            return 30 * math.sqrt(2)
        # If lateral movement, weight is multiplied by 30 * 1
        return 30 * 1
    else:
        # For empty spaces, diagonal weight is sqrt(2) and lateral weight is 1
        if abs(current.x - neighbor.x) == 1 and abs(current.y - neighbor.y) == 1:
            return math.sqrt(2)
        return 1

def lowest_f_score(node_list):
    return min(node_list, key=lambda node: node.f_score)

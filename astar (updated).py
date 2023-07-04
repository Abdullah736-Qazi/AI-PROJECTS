import math
import heapq
import tkinter as tk

# Define the grid dimensions
GRID_WIDTH = 6
GRID_HEIGHT = 6

# Define the size of each grid cell in pixels
CELL_SIZE = 50

# Define the colors
COLOR_GRID = 'black'
COLOR_START = 'green'
COLOR_GOAL = 'red'
COLOR_PATH = 'yellow'
COLOR_EMPTY = 'white'
COLOR_BLOCKED = 'gray'

class Node:
    def __init__(self, x, y, obstacle=False):
        self.x = x
        self.y = y
        self.obstacle = obstacle
        self.g = math.inf
        self.h = math.inf
        self.f = math.inf
        self.parent = None

    def __lt__(self, other):
        return self.f < other.f

def heuristic(node, goal):
    return math.sqrt((node.x - goal.x) ** 2 + (node.y - goal.y) ** 2)

def generate_neighbors(node, grid):
    neighbors = []
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    for dx, dy in directions:
        new_x = node.x + dx
        new_y = node.y + dy
        if 0 <= new_x < len(grid) and 0 <= new_y < len(grid[0]) and not grid[new_x][new_y].obstacle:
            neighbors.append(grid[new_x][new_y])
    return neighbors

def a_star_search(start, goal, grid):
    open_list = []
    closed_set = set()

    start.g = 0
    start.h = heuristic(start, goal)
    start.f = start.h
    heapq.heappush(open_list, start)

    while open_list:
        current = heapq.heappop(open_list)

        if current == goal:
            path = []
            while current:
                path.append((current.x, current.y))
                current = current.parent
            return path[::-1]

        closed_set.add(current)

        neighbors = generate_neighbors(current, grid)
        for neighbor in neighbors:
            if neighbor in closed_set:
                continue

            g_score = current.g + 1
            if g_score < neighbor.g:
                neighbor.g = g_score
                neighbor.h = heuristic(neighbor, goal)
                neighbor.f = neighbor.g + neighbor.h
                neighbor.parent = current

            if neighbor not in open_list:
                heapq.heappush(open_list, neighbor)

    return None

def draw_grid(canvas, grid):
    for i in range(GRID_HEIGHT):
        for j in range(GRID_WIDTH):
            x1 = j * CELL_SIZE
            y1 = i * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE

            if grid[i][j].obstacle:
                color = COLOR_BLOCKED
            else:
                color = COLOR_EMPTY

            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=COLOR_GRID)

def draw_path(canvas, path):
    for i in range(len(path) - 1):
        x1 = path[i][1] * CELL_SIZE + CELL_SIZE // 2
        y1 = path[i][0] * CELL_SIZE + CELL_SIZE // 2
        x2 = path[i + 1][1] * CELL_SIZE + CELL_SIZE // 2
        y2 = path[i + 1][0] * CELL_SIZE + CELL_SIZE // 2

        canvas.create_line(x1, y1, x2, y2, fill=COLOR_PATH, width=3)

def visualize_path(start, goal, grid, path):
    root = tk.Tk()
    root.title("A* Pathfinding Visualization")

    canvas_width = GRID_WIDTH * CELL_SIZE
    canvas_height = GRID_HEIGHT * CELL_SIZE

    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
    canvas.pack()

    draw_grid(canvas, grid)
    canvas.create_rectangle(start.y * CELL_SIZE, start.x * CELL_SIZE,
                            start.y * CELL_SIZE + CELL_SIZE, start.x * CELL_SIZE + CELL_SIZE,
                            fill=COLOR_START, outline=COLOR_START)
    canvas.create_rectangle(goal.y * CELL_SIZE, goal.x * CELL_SIZE,
                            goal.y * CELL_SIZE + CELL_SIZE, goal.x * CELL_SIZE + CELL_SIZE,
                            fill=COLOR_GOAL, outline=COLOR_GOAL)
    draw_path(canvas, path)

    root.mainloop()

# Create the grid
grid = [
    [Node(x, y, obstacle=bool(val)) for y, val in enumerate(row)]
    for x, row in enumerate([
        [0, 1, 0, 0, 1, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 1, 0, 1, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0]
    ])
]

# Define the start and goal locations
start = grid[0][0]
goal = grid[0][5]

# Find the path using A* search
path = a_star_search(start, goal, grid)

# Visualize the path
if path:
    for step in path:
        print(step)
    visualize_path(start, goal, grid, path)
else:
    print("No path found.")

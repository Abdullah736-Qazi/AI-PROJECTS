from collections import deque
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

def generate_neighbors(node, grid):
    neighbors = []
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    for dx, dy in directions:
        new_x = node[0] + dx
        new_y = node[1] + dy
        if 0 <= new_x < len(grid) and 0 <= new_y < len(grid[0]) and not grid[new_x][new_y]:
            neighbors.append((new_x, new_y))
    return neighbors

def bfs(start, goal, grid):
    queue = deque()
    queue.append((start, []))

    while queue:
        current, path = queue.popleft()

        if current == goal:
            return path + [current]

        neighbors = generate_neighbors(current, grid)
        for neighbor in neighbors:
            if grid[neighbor[0]][neighbor[1]] != 1:
                queue.append((neighbor, path + [current]))
                grid[neighbor[0]][neighbor[1]] = 1

    return None

def draw_grid(canvas, grid):
    for i in range(GRID_HEIGHT):
        for j in range(GRID_WIDTH):
            x1 = j * CELL_SIZE
            y1 = i * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE

            if grid[i][j] == 0:
                color = COLOR_EMPTY
            else:
                color = COLOR_BLOCKED

            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=COLOR_GRID)


def draw_path(canvas, path):
    for i in range(len(path) - 1):
        x1 = path[i][1] * CELL_SIZE + CELL_SIZE
        y1 = path[i][0] * CELL_SIZE + CELL_SIZE
        x2 = path[i+1][1] * CELL_SIZE + CELL_SIZE
        y2 = path[i+1][0] * CELL_SIZE + CELL_SIZE

        canvas.create_line(x1, y1, x2, y2, fill=COLOR_PATH, width=3)


def visualize_path(start, goal, grid, path):
    root = tk.Tk()
    root.title("Grid Path Visualization")

    canvas_width = GRID_WIDTH * CELL_SIZE
    canvas_height = GRID_HEIGHT * CELL_SIZE

    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
    canvas.pack()

    draw_grid(canvas, grid)
    canvas.create_oval(start[1] * CELL_SIZE + 5, start[0] * CELL_SIZE + 5,
                       start[1] * CELL_SIZE + CELL_SIZE - 5, start[0] * CELL_SIZE + CELL_SIZE - 5,
                       fill=COLOR_START, outline=COLOR_START)
    canvas.create_oval(goal[1] * CELL_SIZE + 5, goal[0] * CELL_SIZE + 5,
                       goal[1] * CELL_SIZE + CELL_SIZE - 5, goal[0] * CELL_SIZE + CELL_SIZE - 5,
                       fill=COLOR_GOAL, outline=COLOR_GOAL)
    draw_path(canvas, path)

    root.mainloop()


grid = [
    [0, 1, 0, 0, 1, 0],
    [0, 0, 0, 0, 1, 0],
    [0, 0, 1, 0, 1, 0],
    [0, 0, 1, 0, 0, 0],
    [0, 0, 1, 0, 0, 0],
    [0, 0, 1, 0, 0, 0]
]

# Define the start and goal locations
start = (0, 0)
goal = (0, 5)

# Find the path using BFS
path = bfs(start, goal, grid)

# Visualize the path
if path:
    for step in path:
        print(step)
    visualize_path(start, goal, grid, path)
else:
    print("No path found from", start, "to", goal)

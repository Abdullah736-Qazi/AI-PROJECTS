from collections import deque

def is_valid_move(grid, visited, row, col):
    # Check if the move is within the grid boundaries and the cell is not blocked
    num_rows = len(grid)
    num_cols = len(grid[0])
    if row >= 0 and row < num_rows and col >= 0 and col < num_cols and grid[row][col] == 0 and not visited[row][col]:
        return True
    return False

def bfs(grid, start, end):
    num_rows = len(grid)
    num_cols = len(grid[0])
    visited = [[False for _ in range(num_cols)] for _ in range(num_rows)]  # Track visited cells
    queue = deque([(start[0], start[1], [])])  # Initialize the queue with the starting position and an empty path

    # Define the possible moves (up, down, left, right)
    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    while queue:
        row, col, path = queue.popleft()
        visited[row][col] = True

        # Check if the current position is the end position
        if (row, col) == end:
            return path + [(row, col)]  # Return the path to the end position

        # Explore all possible moves
        for move in moves:
            new_row = row + move[0]
            new_col = col + move[1]

            if is_valid_move(grid, visited, new_row, new_col):
                queue.append((new_row, new_col, path + [(row, col)]))

    return None  # No valid path found

# Example usage:
grid = [[0, 1, 0, 0, 1, 0, 0],
        [0, 1, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 1, 0, 0],
        [0, 0, 1, 0, 1, 0, 0],
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0]]

start = (0, 0)
end = (0, 6)

path = bfs(grid, start, end)
if path:
    print("Path found:")
    for position in path:
        print(position)
else:
    print("No valid path found.")

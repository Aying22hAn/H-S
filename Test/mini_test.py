def explore_path(grid, x, y, visited, path):
    # Thêm vị trí hiện tại vào đường đi
    path.append((x, y))
    visited.add((x, y))

    # Định nghĩa 8 hướng có thể di chuyển
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] == 0 and (nx, ny) not in visited:
            explore_path(grid, nx, ny, visited, path)

    return path

# Giả sử grid là mảng 2D đã cho và (x, y) là vị trí bắt đầu
# Tạo một set để lưu trữ các vị trí đã thăm và một list để lưu trữ đường đi
def read_matrix_from_file(file_path):
    matrix = []
    with open(file_path, 'r') as file:
        for line in file:
            row = list(map(int, line.strip().split()))
            matrix.append(row)
    return matrix

matrix = read_matrix_from_file("input1.txt")
visited = set()
path = []

print(path)

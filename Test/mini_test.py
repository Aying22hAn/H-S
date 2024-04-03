def read_matrix_from_file(file_path):
    matrix = []
    with open(file_path, 'r') as file:
        for line in file:
            row = list(map(int, line.strip().split()))
            matrix.append(row)
    return matrix

#x => matrix
#y => matrix[0]
def is_valid_position(matrix, x, y, vision_range, new_x, new_y):
    return ( 
            #Not out of bounds
            (0 <= new_x < len(matrix)) and (0 <= new_y < len(matrix[0]))
            #Not in the same position
            and (new_x != x or new_y != y)
            #In the vision range
            and (abs(new_x - x) <= vision_range and abs(new_y - y) <= vision_range)
            )
def decide_type(x, y, new_x, new_y):
    #same row
    if (new_x == x):
        return 1
    #same column
    elif (new_y == y):
        return 2
    #diagonal
    elif (abs(new_x - x) == abs(new_y - y)):
        return 3
    else:
        return 4
    
matrix = read_matrix_from_file('input.txt')

new_x = 4
new_y = 3
for dx in range(-1,2):
    for dy in range(-1,2):
        if is_valid_position(matrix, 4, 3, 3, new_x + dx, new_y + dy):
            print(decide_type(4, 3, new_x + dx, new_y + dy), end = ' ')
        

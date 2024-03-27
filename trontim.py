import os
import random

# Define constants for map elements
EMPTY = 0
WALL = 1
HIDER = 2
SEEKER = 3

# Define map dimensions
ROWS = 10
COLS = 10

# Function to print the game map
def print_map(map):
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear screen
    for row in map:
        for cell in row:
            if cell == EMPTY:
                print("  ", end="")  # Empty space
            elif cell == WALL:
                print("\033[47m  \033[0m", end="")  # White block (wall)
            elif cell == HIDER:
                print("\033[42mH \033[0m", end="")  # Green H for hider
            elif cell == SEEKER:
                print("\033[41mS \033[0m", end="")  # Red S for seeker
        print()

# Function to check if the given position is within the bounds of the map
def is_valid_position(row, col):
    return 0 <= row < ROWS and 0 <= col < COLS

# Function to check if the given position is a valid move (not a wall)
def is_valid_move(map, row, col):
    return is_valid_position(row, col) and map[row][col] != WALL

# Function to move the seeker randomly
def move_seeker(map, seeker_row, seeker_col):
    # Generate random direction (0: up, 1: down, 2: left, 3: right)
    direction = random.randint(0, 3)
    new_row, new_col = seeker_row, seeker_col

    # Update new position based on direction
    if direction == 0:
        new_row -= 1
    elif direction == 1:
        new_row += 1
    elif direction == 2:
        new_col -= 1
    elif direction == 3:
        new_col += 1

    # Move seeker if the new position is valid
    if is_valid_move(map, new_row, new_col):
        map[seeker_row][seeker_col] = EMPTY
        seeker_row, seeker_col = new_row, new_col
        map[seeker_row][seeker_col] = SEEKER
    return seeker_row, seeker_col

def main():
    # Initialize the game map
    map = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]

    # Set the seeker's initial position
    seeker_row, seeker_col = ROWS // 2, COLS // 2
    map[seeker_row][seeker_col] = SEEKER

    # Set the hider's position
    hider_row, hider_col = 2, 2
    map[hider_row][hider_col] = HIDER

    # Set up walls and obstacles
    map[3][3] = WALL
    map[4][4] = WALL
    map[5][5] = WALL

    # Print the initial map
    print("Initial Map:")
    print_map(map)

    # Game loop
    while True:
        # Move the seeker
        seeker_row, seeker_col = move_seeker(map, seeker_row, seeker_col)

        # Check if seeker found hider
        if (seeker_row == hider_row and abs(seeker_col - hider_col) == 1) or \
           (seeker_col == hider_col and abs(seeker_row - hider_row) == 1):
            print("Seeker caught the hider!")
            break

        # Print updated map
        print("Updated Map:")
        print_map(map)
        input("Press Enter to continue...")

if __name__ == "__main__":
    main()
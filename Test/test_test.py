
import pygame
import sys
import random
import os

''' INITIALIZE GAME CONSOLE '''

# Initialize pygame
pygame.init()
pygame.display.set_caption("Simple Hide & Seek Game")

# Set window size for UI space
width, height = 600, 650
window_screen = pygame.display.set_mode((width, height))

# Color palette
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (50, 50, 50)





# Initial score and time
score = 20 
time_steps = 0

# Temporary agents' position (Have to check if they are stand in valid position)
hiders = []
number_of_hiders = 0
seeker_steps = []
seekers = []
number_of_seekers = 0

# Announcement
# #announcement_icon = pygame.image.load(os.path.join(os.getcwd(), 'announcement.png'))
# announcement_icon = pygame.transform.scale(announcement_icon, (cell_size, cell_size))
# announcements = []
# force_announcement = True

# Temporary obstacles and wall
#obstacles = [(3, 3, 2, 1), (6, 5, 1, 3),(10, 7, 2, 1)] # (x, y, width, height)
#WALL = [(3, 3, 2, 1), (6, 5, 1, 3)] # (x, y, width, height) // Theo truc toa do (x, y)


# Clock for frame rate and timer for seeker's movement delay 
clock = pygame.time.Clock()
moving_time = 0
moving_delay = 300 # Seeker move a step with 1000 ms = 1s

# Font for displaying
font = pygame.font.Font(None, 36)

# Game states
waiting = True
playing = False

























''' Support funtion'''
def draw_text(text, font, color, x, y):
    textobj = font.render(text, True, color)
    window_screen.blit(textobj, (x, y))

def create_button(x, y, function_str):
    # Assuming playing is a boolean indicating the game state
    if playing:
        return

    mouse_position = pygame.mouse.get_pos()
    button_rect = pygame.Rect(x, y, 100, 50)

    # Change button color on hover
    button_color = GREY if button_rect.collidepoint(mouse_position) else WHITE
    pygame.draw.rect(window_screen, button_color, button_rect)

    # Improved text rendering
    text_surface = font.render(function_str, True, BLACK)
    text_rect = text_surface.get_rect(center=button_rect.center)
    window_screen.blit(text_surface, text_rect)



''' FUNCTION FOR AGENT (BACK-END) '''
# Function to check if the given position is within the bounds of the map
def stand_valid_position(row, col):
    if 0 <= row < board_size_height - 2 and 0 <= col < board_size_width - 2:
        # Check for collision with walls
        for wall in walls:
            wall_x, wall_y = wall
            if wall_x == row and wall_y == col:
                return False
        return True
    return False

moving_delay = 50 # Seeker move a step with 1000 ms = 1s
# Function to move the seeker randomly
def move_seeker(position):
    # global number_of_hiders, seeker_steps, force_announcement, seekers
    # #if number_of_hiders == 0:
    # #    return

    # # Generate random direction (0: up, 1: down, 2: left, 3: right)
    # direction = random.randint(0, 3)
    # new_row, new_col = seekers[position][0], seekers[position][1]

    # if direction == 0 and stand_valid_position(new_row - 1, new_col):
    #     new_row -= 1
    # elif direction == 1 and stand_valid_position(new_row + 1, new_col):
    #     new_row += 1
    # elif direction == 2 and stand_valid_position(new_row, new_col - 1):
    #     new_col -= 1
    # elif direction == 3 and stand_valid_position(new_row, new_col + 1):
    #     new_col += 1

    # # Move seeker if the new position is valid
    # seekers[position] = (new_row, new_col)
    # seeker_steps[position] += 1
    # check_for_hiders(seekers[position]) 
    
    ##############################################################################
    global number_of_hiders, seeker_steps, force_announcement, seekers
    #if number_of_hiders == 0:
    #    return

    # Generate random direction (0: up, 1: down, 2: left, 3: right)

    #direction = random.randint(0, 3)
    move = pygame.key.get_pressed()
    new_row, new_col = seekers[position][0], seekers[position][1]    
    if move[pygame.K_w] and stand_valid_position(new_row - 1, new_col):
        new_row -= 1
    elif move[pygame.K_s] and stand_valid_position(new_row + 1, new_col):
        new_row += 1
    elif move[pygame.K_a] and stand_valid_position(new_row, new_col - 1):
        new_col -= 1
    elif move[pygame.K_d] and stand_valid_position(new_row, new_col + 1):
        new_col += 1
        
        
    


    

    # Move seeker if the new position is valid
    seekers[position] = (new_row, new_col)
    seeker_steps[position] += 1
    check_for_hiders(seekers[position]) 
                
def check_for_hiders(seeker):
    global number_of_hiders, score
    # Check if the seeker's position matches any hider's position
    if seeker in hiders:
        score += 10  # Increase the score
        hiders.remove(seeker)  # Remove the found hider from the list
        number_of_hiders -= 1
        if seeker in hider_announcement_timings:  # Safe check before deletion
            del hider_announcement_timings[seeker]  # Remove the timing entry for the found hider
        
        display_game_board()
        create_seeker(seeker, True)
        pygame.display.flip()  # Update the display to reflect changes
        pygame.time.wait(2000)  # Wait a bit to show the found hider
        
        if number_of_hiders == 0:
            return
    

def move_seekers():
    global time_steps, score
    for i in range(number_of_seekers):
        move_seeker(i)
    
    time_steps += 1
    score -= 1

# For vision
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
    
def mark_true_type_1(check, no_vision, vision_range, x, y, new_y):
    if new_y > y:
        
        if(abs(new_y - y) == vision_range
           or abs(new_y - y) == min(y + vision_range, len(check[0]) - 1) - y):
            return
        
        for col in range(new_y + 1, min(y + vision_range + 1, len(check[0]))):
            check[x][col] = True
            no_vision[x][col] = True
        
        if(is_valid_position(check, x, y, vision_range, x + 1, min(y + vision_range, len(check[0]) - 1))):  
            check[x + 1][min(y + vision_range, len(check[0]) - 1)] = True
            no_vision[x + 1][min(y + vision_range, len(check[0]) - 1)] = True 
            
        if(is_valid_position(check, x, y, vision_range, x - 1, min(y + vision_range, len(check[0]) - 1))):  
            check[x - 1][min(y + vision_range, len(check[0]) - 1)] = True
            no_vision[x - 1][min(y + vision_range, len(check[0]) - 1)] = True 
         
    else:
        
        if(abs(new_y - y) == vision_range
              or abs(new_y - y) == y - max(y - vision_range, 0)):
            return
        
        for col in range(max(y - vision_range, 0), new_y):
            check[x][col] = True
            no_vision[x][col] = True
            
            
        if(is_valid_position(check, x, y, vision_range, x + 1, max(y - vision_range, 0))):  
            check[x + 1][max(y - vision_range, 0)] = True
            no_vision[x + 1][max(y - vision_range, 0)] = True
            
        if(is_valid_position(check, x, y, vision_range, x - 1, max(y - vision_range, 0))):  
            check[x - 1][max(y - vision_range, 0)] = True
            no_vision[x - 1][max(y - vision_range, 0)] = True  
                                
def mark_true_type_2(check, no_vision, vision_range, x, y, new_x):
    if new_x > x:
        if((abs(new_x - x) == vision_range)
           or (abs(new_x - x) == min(x + vision_range, len(check) - 1) - x)):
            return
        
        for col in range(new_x + 1, min(x + vision_range + 1, len(check))):
            check[col][y] = True
            no_vision[col][y] = True
        
        if(is_valid_position(check, x, y, vision_range, min(x + vision_range, len(check) - 1), y + 1)):
            check[min(x + vision_range, len(check) - 1)][y + 1] = True
            no_vision[min(x + vision_range, len(check) - 1)][y + 1] = True
            
        if(is_valid_position(check, x, y, vision_range, min(x + vision_range, len(check) - 1), y - 1)): 
            check[min(x + vision_range, len(check) - 1)][y - 1] = True
            no_vision[min(x + vision_range, len(check) - 1)][y - 1] = True
        
    else:
        
        if((abs(new_x - x) == vision_range)
              or (abs(new_x - x) == x - max(x - vision_range, 0))):
                return
            
        for col in range(max(x - vision_range, 0), new_x):
            check[col][y] = True
            no_vision[col][y] = True
            
        if(is_valid_position(check, x, y, vision_range, max(x - vision_range, 0), y + 1)): 
            check[max(x - vision_range, 0)][y + 1] = True
            no_vision[max(x - vision_range, 0)][y + 1] = True
            
        if(is_valid_position(check, x, y, vision_range, max(x - vision_range, 0), y - 1)):    
            check[max(x - vision_range, 0)][y - 1] = True
            no_vision[max(x - vision_range, 0)][y - 1] = True
            
def mark_true_type_3(check, no_vision, vision_range, x, y, new_x, new_y):
    if (new_x > x and new_y > y):#Quadrant IV
        if((abs(new_x - x) == vision_range) 
           or (abs(new_x - x) == min(x + vision_range, len(check) - 1) - x) 
            or (abs(new_x - x) == min(y + vision_range, len(check[0]) - 1) - y)):
            return
        
        for i in range(1, vision_range):
            if is_valid_position(check, x, y, vision_range, new_x + i, new_y + i):
                check[new_x + i][new_y + i] = True
                no_vision[new_x + i][new_y + i] = True
        
        if(abs((min(x + vision_range, len(check) - 1) - x)) == abs(min(y + vision_range, len(check[0]) - 1) - y)):
            check[min(x + vision_range, len(check) - 1)][min(y + vision_range, len(check[0]) - 1)] = True
            check[min(x + vision_range, len(check) - 1)][min(y + vision_range, len(check[0]) - 1) - 1] = True
            check[min(x + vision_range, len(check) - 1) - 1][min(y + vision_range, len(check[0]) - 1)] = True
            no_vision[min(x + vision_range, len(check) - 1)][min(y + vision_range, len(check[0]) - 1)] = True
            no_vision[min(x + vision_range, len(check) - 1)][min(y + vision_range, len(check[0]) - 1) - 1] = True
            no_vision[min(x + vision_range, len(check) - 1) - 1][min(y + vision_range, len(check[0]) - 1)] = True
        
            
    elif (new_x < x and new_y < y):#Quadrant II
        
        if((abs(new_x - x) == vision_range) 
           or (abs(new_x - x) == x - max(x - vision_range, 0)) 
            or (abs(new_x - x) == y - max(y - vision_range, 0))):
            return
        
        for i in range(1, vision_range):
            if is_valid_position(check, x, y, vision_range, new_x - i, new_y - i):
                check[new_x - i][new_y - i] = True
                no_vision[new_x - i][new_y - i] = True
        
        if(abs(max(x - vision_range, 0) - x) == abs(max(y - vision_range, 0) - y)):        
            check[max(x - vision_range, 0)][max(y - vision_range, 0)] = True
            check[max(x - vision_range, 0) + 1][max(y - vision_range, 0)] = True
            check[max(x - vision_range, 0)][max(y - vision_range, 0) + 1] = True
            no_vision[max(x - vision_range, 0)][max(y - vision_range, 0)] = True
            no_vision[max(x - vision_range, 0) + 1][max(y - vision_range, 0)] = True
            no_vision[max(x - vision_range, 0)][max(y - vision_range, 0) + 1] = True
              
        
    elif (new_x > x and new_y < y):#Quadrant III
        
        if((abs(new_x - x) == vision_range) 
           or (abs(new_x - x) == min(x + vision_range, len(check) - 1) - x) 
            or (abs(new_x - x) == y - max(y - vision_range, 0))):
            return
        
        for i in range(1, vision_range):
            if is_valid_position(check, x, y, vision_range, new_x + i, new_y - i):
                check[new_x + i][new_y - i] = True
                no_vision[new_x + i][new_y - i] = True
        
        if(abs(min(x + vision_range, len(check) - 1) - x) == abs(max(y - vision_range, 0) - y)):    
            check[min(x + vision_range, len(check) - 1)][max(y - vision_range, 0)] = True
            check[min(x + vision_range, len(check) - 1)][max(y - vision_range, 0) + 1] = True
            check[min(x + vision_range, len(check) - 1) - 1][max(y - vision_range, 0)] = True
            no_vision[min(x + vision_range, len(check) - 1)][max(y - vision_range, 0)] = True
            no_vision[min(x + vision_range, len(check) - 1)][max(y - vision_range, 0) + 1] = True
            no_vision[min(x + vision_range, len(check) - 1) - 1][max(y - vision_range, 0)] = True
            
        
    else:#Quadrant I
        
        if((abs(new_x - x) == vision_range) 
           or (abs(new_x - x) == x - max(x - vision_range, 0)) 
            or (abs(new_x - x) == min(y + vision_range, len(check[0]) - 1) - y)):
            return
        
        for i in range(1, vision_range):
            if is_valid_position(check, x, y, vision_range, new_x - i, new_y + i):
                check[new_x - i][new_y + i] = True
                no_vision[new_x - i][new_y + i] = True
        
        if(abs(max(x - vision_range, 0) - x) == abs(min(y + vision_range, len(check[0]) - 1) - y)):    
            check[max(x - vision_range, 0)][min(y + vision_range, len(check[0]) - 1)] = True
            check[max(x - vision_range, 0)][min(y + vision_range, len(check[0]) - 1) - 1] = True
            check[max(x - vision_range, 0) + 1][min(y + vision_range, len(check[0]) - 1)] = True
            no_vision[max(x - vision_range, 0)][min(y + vision_range, len(check[0]) - 1)] = True
            no_vision[max(x - vision_range, 0)][min(y + vision_range, len(check[0]) - 1) - 1] = True
            no_vision[max(x - vision_range, 0) + 1][min(y + vision_range, len(check[0]) - 1)] = True      
                
def mark_true_type_4(check, no_vision, vision_range, x, y, new_x, new_y):
    if(new_x < x and new_y > y): #Quadrant I
        if(abs(new_x - x) > abs(new_y - y)):
            count = 1 #mark triangle
            for row in range(new_x, max(-1, x - vision_range - 1), -1):
                for dy in range(count):
                    if is_valid_position(check, x, y, vision_range, row, new_y + dy):
                        check[row][new_y + dy] = True
                        no_vision[row][new_y + dy] = True
                        
                count += 1
        else:
            count = 1
            for col in range(new_y, min(len(check[0]), y + vision_range + 1)):
                for dx in range(count):
                    if is_valid_position(check, x, y, vision_range, new_x - dx, col):
                        check[new_x - dx][col] = True
                        no_vision[new_x - dx][col] = True
                        
                count += 1
                
    elif(new_x < x and new_y < y): #Quadrant II
        if(abs(new_x - x) > abs(new_y - y)):
            count = 1
            for row in range(new_x, max(-1, x - vision_range - 1), -1):
                for dy in range(count):
                    if is_valid_position(check, x, y, vision_range, row, new_y - dy):
                        check[row][new_y - dy] = True
                        no_vision[row][new_y - dy] = True
                        
                count += 1
        else:
            count = 1
            for col in range(new_y, max(-1, y - vision_range - 1), -1):
                for dx in range(count):
                    if is_valid_position(check, x, y, vision_range, new_x - dx, col):
                        check[ new_x - dx][col] = True
                        no_vision[ new_x - dx][col] = True
                        
                count += 1            
    elif(new_x > x and new_y < y):#Quadrant III
        if(abs(new_x - x) > abs(new_y - y)):
            count = 1
            for row in range(new_x, min(len(check), x + vision_range + 1)):
                for dy in range(count):
                    if is_valid_position(check, x, y, vision_range, row, new_y - dy):
                        check[row][new_y - dy] = True
                        no_vision[row][new_y - dy] = True
                        
                count += 1
        else:
            count = 1
            for col in range(new_y, max(-1, y - vision_range - 1), -1):
                for dx in range(count):
                    if is_valid_position(check, x, y, vision_range, new_x + dx, col):
                        check[new_x + dx][col] = True
                        no_vision[new_x + dx][col] = True
                        
                count += 1
    else: #Quadrant IV
        if(abs(new_x - x) > abs(new_y - y)):
            count = 1
            for row in range(new_x, min(len(check), x + vision_range + 1)):
                for dy in range(count):
                    if is_valid_position(check, x, y, vision_range, row, new_y + dy):
                        check[row][new_y + dy] = True
                        no_vision[row][new_y + dy] = True
                        
                count += 1
        else:
            count = 1
            for col in range(new_y, min(len(check[0]), y + vision_range + 1)):
                for dx in range(count):
                    if is_valid_position(check, x, y, vision_range, new_x + dx, col):
                        check[new_x + dx][col] = True
                        no_vision[new_x + dx][col] = True
                        
                count += 1  

def check_surrounding(no_vision, x, y, new_x, new_y, vision_range):
    cross = 0
                 
    for(dx, dy) in [(-1,0), (1,0), (0,-1), (0,1)]:
        if((max(0, x - vision_range) <= new_x + dx < min(len(matrix), x + vision_range + 1)) 
           and (max(0, y - vision_range) <= new_y + dy < min(len(matrix[0]), y + vision_range + 1))
           and no_vision[new_x + dx][new_y + dy] == True):
            cross = cross + 1
    
    if(cross == 4):
        return True    
    
    if(new_x < x and new_y > y):
        if(no_vision[new_x + 1][new_y] == True and no_vision[new_x][new_y - 1] == True):
            return True
        
    elif(new_x < x and new_y < y):
        if(no_vision[new_x + 1][new_y] == True and no_vision[new_x][new_y + 1] == True):
            return True
    
    elif(new_x > x and new_y < y):
        if(no_vision[new_x - 1][new_y] == True and no_vision[new_x][new_y + 1] == True):
            return True
    
    elif(new_x > x and new_y > y):
        if(no_vision[new_x - 1][new_y] == True and no_vision[new_x][new_y - 1] == True):
            return True
    
    return False 

def flood_fill(matrix, check, no_vision, x, y, new_x, new_y, vision_range):
    
    check[new_x][new_y] = True
    
    for dx in range(-1,2):
        for dy in range(-1,2):
            if is_valid_position(matrix, x, y, vision_range, new_x + dx, new_y + dy):
                if(check[new_x + dx][new_y + dy] == False):
                    check[new_x + dx][new_y + dy] = True
                    if (matrix[new_x + dx][new_y + dy] == 1):
                        no_vision[new_x + dx][new_y + dy] = True
                        if(decide_type(x, y, new_x + dx, new_y + dy) == 1):
                            mark_true_type_1(check, no_vision, vision_range, x, y, new_y + dy)
                        elif(decide_type(x, y, new_x + dx, new_y + dy) == 2):
                            mark_true_type_2(check, no_vision, vision_range, x, y, new_x + dx)
                        elif(decide_type(x, y, new_x + dx, new_y + dy) == 3):
                            mark_true_type_3(check, no_vision, vision_range, x, y, new_x + dx, new_y + dy)
                        elif(decide_type(x, y, new_x + dx, new_y + dy) == 4):
                            mark_true_type_4(check, no_vision, vision_range, x, y, new_x + dx, new_y + dy)             
                    else:
                        flood_fill(matrix, check, no_vision, x, y, new_x + dx, new_y + dy, vision_range)
 
def mark_vision(matrix, x, y, vision_range):
    
    
    check = []
    check = [[False] * len(matrix[0]) for _ in range(len(matrix))]
                
    no_vision = []
    no_vision = [[False] * len(matrix[0]) for _ in range(len(matrix))]
    
    flood_fill(matrix, check, no_vision, x, y, x, y, vision_range)
    
    for row in range(max(0, x - vision_range), min(len(matrix), x + vision_range + 1)):
        for col in range(max(0, y - vision_range), min(len(matrix[0]), y + vision_range + 1)):
            if(row != x and col != y and check_surrounding(no_vision, x, y, row, col, vision_range) == True):
                no_vision[row][col] = True
    
    return check, no_vision


''' File Handling '''
def read_matrix_from_file(file_path):
    matrix = []
    with open(file_path, 'r') as file:
        for line in file:
            row = list(map(int, line.strip().split()))
            matrix.append(row)
    return matrix

matrix = read_matrix_from_file('input.txt')

# Game board setting
board_size = 10
board_size_height = len(matrix) + 2
board_size_width = len(matrix[0]) + 2
cell_size = min(width // board_size_width - 2, height // board_size_height - 2)



# Find position of walls, hiders, and seekers
walls = [(row_index, col_index) for row_index, row in enumerate(matrix) for col_index, cell in enumerate(row) if cell == 1] 
hiders = [(row_index, col_index) for row_index, row in enumerate(matrix) for col_index, cell in enumerate(row) if cell == 2] 
seekers = [(row_index, col_index) for row_index, row in enumerate(matrix) for col_index, cell in enumerate(row) if cell == 3]
# Count the number of hiders and seekers
number_of_hiders = len(hiders)
number_of_seekers = len(seekers)
seeker_steps = [0 for i in range(number_of_seekers)]


'''
with open("output.txt", "w") as file:
    for row in no_vision:
        for col in row:
            file.write(str(int(col)) + ' ')
        file.write('\n')
    file.write('\n')
    
    for row in check:
        for col in row:
            file.write(str(int(col)) + ' ')
        file.write('\n')
'''   

















''' DRAW GAME BOARD '''
# Function to create game board, hiders, and seeker
def make_grid():
    # Calculate the number of cells that can fit in the x and y directions
    num_cells_x = board_size_height - 2
    num_cells_y = board_size_width - 2
    if num_cells_x != board_size_height - 2:
        if num_cells_x < board_size_height - 2:
            num_cells_x += 1
        else: num_cells_x -= 1
        
    if num_cells_y != board_size_width - 2:
        if num_cells_y < board_size_width - 2:
            num_cells_y += 1
        else: num_cells_y -= 1

    for x in range(num_cells_x):
        for y in range(num_cells_y):
            # Calculate the top-left corner of each cell
            cell_x = cell_size + x * cell_size
            cell_y = cell_size + y * cell_size

            # Create a rectangle for the cell
            rect = pygame.Rect(cell_x, cell_y, cell_size, cell_size)

            # Draw the cell on the window screen with a grey border
            pygame.draw.rect(window_screen, (170, 170, 170), rect, 1)


def create_obstacles(obstacles):
    for obstacle in obstacles:
        
        left = (obstacle[1] + 1) * cell_size
        top = (obstacle[0] + 1) * cell_size
        wid = cell_size
        hei = cell_size
        rect = pygame.Rect(left, top, wid, hei)
        pygame.draw.rect(window_screen, GREY, rect)
        
def create_hider(hider):
    #show_observation_range(hider)
    center_y, center_x = (hider[0] + 1) * cell_size + cell_size // 2 , (hider[1] + 1) * cell_size + cell_size // 2
    pygame.draw.circle(window_screen, RED, (center_x, center_y), cell_size // 2 - cell_size // 3.5)

def create_hiders():
    i = 0
    while i < number_of_hiders:
        hider = (random.randint(1,board_size_height + 1), random.randint(1,board_size_width + 1))
        if stand_valid_position(hider[0], hider[1]):
            hiders.append(hider)
            i += 1
        
def display_hiders():
    for i in range (number_of_hiders):
        create_hider(hiders[i])
    
def create_seeker(seeker, found = False):
    color = GREEN if found else BLUE
    show_observation_range(seeker, 3)
    center_y, center_x = (seeker[0] + 1) * cell_size + cell_size // 2, (seeker[1] + 1) * cell_size + cell_size // 2
    pygame.draw.circle(window_screen, color, (center_x, center_y), cell_size // 2 - cell_size // 3.5)    
    
def create_seekers():
    i = 0
    while i < number_of_seekers:
        seeker = (random.randint(1,board_size_height + 1), random.randint(1,board_size_width + 1))
        if stand_valid_position(seeker[0], seeker[1]):
            seekers.append(seeker)
            seeker_steps.append(0)
            i += 1       
    
def display_seekers():
    for i in range (number_of_seekers):
        create_seeker(seekers[i])

            
def create_announcement(x, y):
    # Calculate the pixel position
    pixel_x = (x + 1) * cell_size
    pixel_y = (y + 1) * cell_size
    # Draw the announcement icon at the specified position
    window_screen.blit(announcement_icon, (pixel_x, pixel_y))
    
#def display_announcement():
#    for announce_x, announce_y in announcements:  # Corrected iteration
#        create_announcement(announce_x, announce_y)
    
# Function to display console  
def display_score_and_time():
    draw_text(f"Score: {score}", font, WHITE, 20, height - 40)
    draw_text(f"Time: {time_steps}", font, WHITE, width - 150, height - 40 )
    
def display_game_board():
    window_screen.fill(BLACK)
    
    # Then, draw a white rectangle over the area where the game is played
    play_area_rect = pygame.Rect(0, 0, width , height - 50)  # Subtract 50 to leave space for the time and score
    pygame.draw.rect(window_screen, (230, 230, 230), play_area_rect)
    make_grid()
    create_obstacles(walls)
    display_hiders()
    display_seekers()
    display_score_and_time()


''' Start and Finish Console'''
def display_finish_console():
    overlay = pygame.Surface((width, height), pygame.SRCALPHA) # SRCALPHA  for transparency
    overlay.fill((0, 0, 0, 128)) # Semi-transparent black overlay
    window_screen.blit(overlay, (0, 0))
    
    found_font = pygame.font.Font(None, 50)
    score_font = pygame.font.Font(None, 36)
    message_surface = found_font.render("The hider is found!", True, WHITE)
    score_surface = score_font.render(f"Score: {score}", True, WHITE)
    message_rect = message_surface.get_rect(center=(width / 2, height / 2))
    score_rect = score_surface.get_rect(center = (width / 2, height / 2 + 40 ))
    window_screen.blit(message_surface, message_rect)
    window_screen.blit(score_surface, score_rect)
    pygame.display.flip() # Update window console
    pygame.time.delay(10000) # Show
 
def start_console():
    create_button((width - 100) // 2, (height - 50) // 2, "Start")
    title_font = pygame.font.SysFont("Comic Sans MS", 70)
    title_surface = title_font.render("HIDE & SEEK", True, (0, 207, 207))
    title_rect = title_surface.get_rect(center = (width / 2, 120))
    window_screen.blit(title_surface, title_rect)
 
 
''' Observation range UI'''
def darken_cell(x, y):
    rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
    surface = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
    surface.fill((0, 0, 0, 30))  # Semi-transparent overlay
    window_screen.blit(surface, rect.topleft)
    pass

def show_observation_range(position, range_limit = 3):
    check, no_vision = mark_vision(matrix, position[0], position[1], range_limit)
    
    for dx in range(-range_limit, range_limit + 1):
        for dy in range(-range_limit, range_limit + 1):
            # Calculate the cell's position relative to the agent
            cell_x = position[1] + dx
            cell_y = position[0] + dy
            # Ensure the cell is within the game board boundaries
                
            if 0 <= cell_y < len(matrix) and 0 <= cell_x < len(matrix[0]):
                if no_vision[cell_y][cell_x] != 1:
                    darken_cell(cell_x + 1, cell_y + 1)  # Adjust for grid off

    


 
last_click_time = 0

while True:
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if current_time - last_click_time > 0:  # Check if enough time has passed
                last_click_time = current_time  # Update the last click time
                mouse_pos = event.pos  # Get the mouse position
                button_rect = pygame.Rect((width - 100) // 2, (height - 50) // 2, 100, 50)
                if button_rect.collidepoint(mouse_pos) and waiting:
                    waiting = False
                    playing = True
                    #create_hiders()
                    #create_seekers()
                    hider_announcement_timings = {hider: random.randint(5, 10) for hider in hiders}
                    
    window_screen.fill(BLACK)
    if waiting:
        start_console()
    elif playing:
        if number_of_hiders == 0:
            waiting = True
            playing = False
            display_finish_console()
            break
            
        else:
            display_game_board()
            if current_time - moving_time > moving_delay:
                moving_time = current_time
                move_seekers()
                
    pygame.display.flip()
    clock.tick(10000)
    

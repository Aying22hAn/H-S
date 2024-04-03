import pygame
import sys
import random
import os

''' INITIALIZE GAME CONSOLE '''

# Initialize pygame
pygame.init()
pygame.display.set_caption("Simple Hide & Seek Game")

# Set window size for UI space
width, height = 700, 750
window_screen = pygame.display.set_mode((width, height))

# Color palette
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (50, 50, 50)

# Game board setting
board_size = 10
cell_size = width // board_size
score = 20 
time_steps = 0

# Temporary agents' position (Have to check if they are stand in valid position)
hiders = []
number_of_hiders = 5
seeker_steps = 0
seeker = (0, 0)

# Announcement
announcement_icon = pygame.image.load(os.path.join(os.getcwd(), 'announcement.png'))
announcement_icon = pygame.transform.scale(announcement_icon, (cell_size, cell_size))
announcements = []
force_announcement = True

# Temporary obstacles and wall
#obstacles = [(3, 3, 2, 1), (6, 5, 1, 3),(10, 7, 2, 1)] # (x, y, width, height)
WALL = [(3, 3, 2, 1), (6, 5, 1, 3),(10, 7, 2, 1)] # (x, y, width, height) // Theo truc toa do (x, y)


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


''' DRAW GAME BOARD '''
# Function to create game board, hiders and seeker
def make_grid():
    for x in range(cell_size, width - cell_size, cell_size):
        for y in range(cell_size, height - 50 - cell_size, cell_size): # Minus 50 to leave space for time and score display
            rect = pygame.Rect(x, y, cell_size, cell_size) # For storing rectangular coordinates
            pygame.draw.rect(window_screen, (170, 170, 170), rect, 1) # To draw a cell on window screen with grey color

def create_obstacles(obstacles):
    for obstacle in obstacles:
        left = (obstacle[0] + 1) * cell_size
        top = (obstacle[1] + 1) * cell_size
        wid = obstacle[2] * cell_size
        hei = obstacle[3] * cell_size
        rect = pygame.Rect(left, top, wid, hei)
        pygame.draw.rect(window_screen, GREY, rect)
        
def create_hider(hider):
    center_x, center_y = (hider[0] + 1) * cell_size + cell_size // 2 , (hider[1] + 1) * cell_size + cell_size // 2
    pygame.draw.circle(window_screen, RED, (center_x, center_y), cell_size // 2 - cell_size // 3.5)

def create_hiders():
    i = 0
    while i < number_of_hiders:
        hider = (random.randint(1,board_size - 3), random.randint(1,board_size - 3))
        if is_valid_position(hider[0], hider[1]):
            hiders.append(hider)
            i += 1
        
def display_hiders():
    for i in range (number_of_hiders):
        create_hider(hiders[i])
    
def display_seeker(found = False):
    color = GREEN if found else BLUE
    show_observation_range(seeker, 3)
    center_x, center_y = (seeker[0] + 1) * cell_size + cell_size // 2, (seeker[1] + 1) * cell_size + cell_size // 2
    pygame.draw.circle(window_screen, color, (center_x, center_y), cell_size // 2 - cell_size // 3.5)

# Function to handle announcements
#def handle_announcements(range_limit, force=False):
#    global announcements, seeker_steps

    # Condition to make new announcements
#    if seeker_steps >= 5 or force:
#        announcements.clear()  # Clear existing announcements if making new ones
#        for hider in hiders:
#            valid = False
#            while not valid:
#                announce_x = random.randint(max(1, hider[0] - range_limit), min(board_size - 2, hider[0] + range_limit))
#                announce_y = random.randint(max(1, hider[1] - range_limit), min(board_size - 2, hider[1] + range_limit))

#                if is_valid_position(announce_x, announce_y):
#                    duration = random.randint(5, 10)  # Duration for this announcement
#                    announcements.append(((announce_x, announce_y), duration))
#                    valid = True
#        seeker_steps = 0  # Reset after making announcements
#    else:
#        # Decrement duration of each announcement, remove if expired
#        announcements = [((x, y), time - 1) for (x, y), time in announcements if time > 1]
#
#    # Always attempt to display current valid announcements
#    display_announcement()

                    
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
    
def display_game_board(found):
    window_screen.fill(BLACK)
    
    # Then, draw a white rectangle over the area where the game is played
    play_area_rect = pygame.Rect(0, 0, width , height - 50)  # Subtract 50 to leave space for the time and score
    pygame.draw.rect(window_screen, (230, 230, 230), play_area_rect)
    make_grid()
    create_obstacles(WALL)
    display_hiders()
    display_seeker(found)
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
 
 
''' Observation range'''
def darken_cell(x, y):
    rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
    surface = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
    surface.fill((0, 0, 0, 30))  # Semi-transparent overlay
    window_screen.blit(surface, rect.topleft)

def show_observation_range(position, range_limit = 3):
    for dx in range(-range_limit, range_limit + 1):
        for dy in range(-range_limit, range_limit + 1):
            #if dx == 0 and dy == 0:
            #    continue
            # Calculate the cell's position relative to the agent
            cell_x = position[0] + dx
            cell_y = position[1] + dy
            # Ensure the cell is within the game board boundaries
            ''' Sẽ thêm điều kiện quan sát của agent của bên back-end team '''
            if 0 <= cell_x < board_size - 2 and 0 <= cell_y < board_size - 2:
                darken_cell(cell_x + 1, cell_y + 1)  # Adjust for grid off



''' FUNCTION FOR AGENT '''
# Function to check if the given position is within the bounds of the map
def is_valid_position(row, col):
    if 0 <= row < board_size - 2 and 0 < col < board_size - 2:
        # Check for collision with walls
        for wall in WALL:
            wall_x, wall_y, wall_width, wall_height = wall
            if wall_x <= row < wall_x + wall_width and wall_y <= col < wall_y + wall_height:
                return False
        return True
    
    return False


# Function to move the seeker randomly
def move_seeker():
    global number_of_hiders, seeker, time_steps, score, seeker_steps, force_announcement
    #if number_of_hiders == 0:
    #    return

    # Generate random direction (0: up, 1: down, 2: left, 3: right)
    direction = random.randint(0, 3)
    new_row, new_col = seeker[0], seeker[1]

    if direction == 0 and is_valid_position(new_row - 1, new_col):
        new_row -= 1
    elif direction == 1 and is_valid_position(new_row + 1, new_col):
        new_row += 1
    elif direction == 2 and is_valid_position(new_row, new_col - 1):
        new_col -= 1
    elif direction == 3 and is_valid_position(new_row, new_col + 1):
        new_col += 1

    # Move seeker if the new position is valid
    seeker = (new_row, new_col)
    time_steps += 1
    seeker_steps += 1
    score -= 1
    check_for_hiders() 
                
def check_for_hiders():
    global number_of_hiders, score
    # Check if the seeker's position matches any hider's position
    if seeker in hiders:
        score += 10  # Increase the score
        hiders.remove(seeker)  # Remove the found hider from the list
        number_of_hiders -= 1
        if seeker in hider_announcement_timings:  # Safe check before deletion
            del hider_announcement_timings[seeker]  # Remove the timing entry for the found hider
            
        if number_of_hiders == 0:
            return
        display_game_board(True)
        pygame.display.flip()  # Update the display to reflect changes
        pygame.time.wait(2000)  # Wait a bit to show the found hider
        display_game_board(False)  # Possibly refresh the game board to continue playing
        pygame.display.flip()  # Update the display again

 
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
                    create_hiders()
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
            display_game_board(False)
            if current_time - moving_time > moving_delay:
                moving_time = current_time
                move_seeker()
                
    pygame.display.flip()
    clock.tick(10000)
    
import random

class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]  
        self.seeker_pos = (0, 0)  
        self.hider_pos = (random.randint(0, width-1), random.randint(0, height-1))  

    def place_wall(self, x, y):
        self.board[y][x] = 1  

    def move_seeker(self, direction):
        x, y = self.seeker_pos
        dx, dy = direction
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < self.width and 0 <= new_y < self.height and self.board[new_y][new_x] != 1:
            self.seeker_pos = (new_x, new_y)

    def catch_hider(self):
        return self.seeker_pos == self.hider_pos

    def print_board(self):
        for row in self.board:
            print(''.join(['#' if cell == 1 else '.' for cell in row]))

def main():
    width, height = 10, 10  
    game = Game(width, height)
    game.place_wall(2, 2) 
    
    while True:
        game.print_board()
        direction = input("Enter direction (WASD): ").upper()
        if direction == 'W':
            game.move_seeker((0, -1))
        elif direction == 'S':
            game.move_seeker((0, 1))
        elif direction == 'A':
            game.move_seeker((-1, 0))
        elif direction == 'D':
            game.move_seeker((1, 0))
        else:
            print("Invalid input. Please enter W, A, S, or D.")
            continue
        
        if game.catch_hider():
            print("Hider caught! Game over.")
            break

if __name__ == "__main__":
    main()
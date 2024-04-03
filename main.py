#UI need to modify this class to get the color code for each cell
class Cell:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
class EmptyCell(Cell):
    def __init__(self, x, y, type):
        super().__init__(x, y, type)
        
        
        
class Agent(Cell):
    
    def __init__(self, x, y, type, map):
        super().__init__(x, y, type)
        self.map = map
        
    def move(self, dx, dy):
        super().move(dx, dy)
        self.x += dx
        self.y += dy

class Seeker(Agent):
    pass

class Hider(Agent):
    pass

class BoardGame:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[Cell(0, 0, 0) for _ in range(width)] for _ in range(height)]
        self.obstacles = []

    def initialize_from_file(self, file_path):
        with open(file_path, 'r') as file:
            # Read the size of the map
            height, width  = map(int, file.readline().split())

            # Update the board size
            self.width = width
            self.height = height
            self.board = [[Cell(0, 0, 0) for _ in range(width)] for _ in range(height)]

            # Read the map matrix
            for i in range(height):
                row = list(map(int, file.readline().split()))
                self.board[i] = [Cell(i, j, cell_type) for j, cell_type in enumerate(row)]
                

            # Read the obstacle coordinates
            coordinates = []
            for line in file:
                x1, y1, x2, y2 = map(int, line.split())
                coordinates.append(((x1, y1), (x2, y2)))
            
            self.obstacles = coordinates
            
    def print_boardgame_properties(self):
        print(self.height, end=' ')
        print(self.width, end=' ')
        print()
        for i in range(self.height):
            for j in range(self.width):
                print(self.board[i][j].type, end=' ')
            print()
        for coordinate in self.obstacles:
            print(coordinate, end=' ')
            print()

class HideAndSeekGame:
    def __init__(self, width, height, max_steps, vision_range):
        self.map = BoardGame.initialize_from_file('input.txt')
        self.max_steps = max_steps
        self.steps_taken = 0
        self.vision_range = vision_range
        
    def seeker_vision(self):
        for i in range(-self.vision_range, self.vision_range + 1):
            for j in range(-self.vision_range, self.vision_range + 1):
                if 0 <= seeker.x + i < self.map.width and 0 <= seeker.y + j < self.map.height:
                    vision.append(self.map.board[seeker.y + j][seeker.x + i])
        return vision
         
    
    
                
def main():
    # Create an instance of BoardGame
    game = BoardGame(0, 0)

    # Initialize the game from input.txt
    game.initialize_from_file('input.txt')

    # Print the properties of the game
    game.print_boardgame_properties()

# Call the main function
if __name__ == '__main__':
    main()
    

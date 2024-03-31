#UI need to modify this class to get the color code for each cell
class Cell:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.color = None # set up color depending on the type of cell

class Map:
    def __init__(self, height, width, board, obstacles):
        self.height = height
        self.width = width
        self.board = board
        self.obstacles = obstacles

    
class Agent(Cell):
    
    def __init__(self, x, y, type, map):
        super().__init__(x, y, type)
        self.map = map
        
    

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
    #UI need to modify this function to get the color code for each cell
    def set_color_for_obstacle(self):
        for coordinate in self.obstacles:
            x1, y1 = coordinate[0]
            x2, y2 = coordinate[1]
            for i in range(x1, x2 + 1):
                for j in range(y1, y2 + 1):
                    self.board[i][j].color = 'black' # temp color(will be replace by color code)    
    
    def create_map(self):
        # Create an instance of Map
        map = Map(self.height, self.width, [[cell.type for cell in row] for row in self.board], self.obstacles)
        return map
    
    
                
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
    

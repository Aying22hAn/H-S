def read_matrix_from_file(file_path):
    matrix = []
    with open(file_path, 'r') as file:
        for line in file:
            row = list(map(int, line.strip().split()))
            matrix.append(row)
    return matrix


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
    
    
# def write_matrix_to_file(file_path, matrix):
#     with open(file_path, 'a') as file:
#         for row in matrix:
#             file.write(' '.join(map(str, [int(col) for col in row])) + '\n')
#         file.write('\n')
    
def print_matrix(matrix):
    for row in matrix:
        for col in row:
            print(int(col), end = ' ')
        print()
    print()
        
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

matrix = read_matrix_from_file('input1.txt')


while(True):
    chr = input()
    if chr == 'q':
        break
    else:
        x, y = int(input()), int(input())
        
        check, no_vision = mark_vision(matrix, x, y, 3)

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
                
           

            

    
    
  
    
    




    
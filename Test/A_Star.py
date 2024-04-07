import math

class Node:
    def __init__(self, parent = None, position = None):
        self.parent = parent
        self.position = position
        self.f = 0
        self.g = 0
        self.h = 0

'''Quy ước trên map:
        Giá trị 0: chưa kiểm tra đến
        Giá trị 1: chướng ngại vật
        Giá trị 2: có thể đi đến (node con)
        Giá trị 3: đã từng đi qua
    Kết quả có thể lấy được từ hàm là 1 map đã đánh dấu quá trình duyệt và node cuối cùng mà ta có thể truy ngược về node cha để lấy đường dẫn'''
def A_Star(map, startNode, endNode):
    openList = [startNode]
    closedList = []

    while openList:
        currentNode = openList[0]
        currentIndex = 0

        # Find the node with the lowest f value in the open list
        for index, node in enumerate(openList):
            if node.f < currentNode.f:
                currentNode = node
                currentIndex = index

        # Move the current node from the open list to the closed list
        openList.pop(currentIndex)
        closedList.append(currentNode)

        # Check if the current node is the end node
        if currentNode.position == endNode.position:
            return currentNode

        # Generate the children nodes
        children = []
        for move in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            move_to = (currentNode.position[0] + move[0], currentNode.position[1] + move[1])
            if move_to[0] >= 0 and move_to[0] < len(map) and move_to[1] >= 0 and move_to[1] < len(map[0]) and map[move_to[0]][move_to[1]] == 0:
                childNode = Node(currentNode, move_to)
                children.append(childNode)

        # Calculate the g, h, and f values for each child node
        for child in children:
            child.g = currentNode.g + math.sqrt((child.parent.position[0] - child.position[0])**2 + (child.parent.position[1] - child.position[1])**2)
            dx = abs(child.position[0] - endNode.position[0])
            dy = abs(child.position[1] - endNode.position[1])
            child.h = (dx + dy) + (math.sqrt(2) - 2) * min(dx, dy)
            child.f = child.g + child.h

            # Check if the child node is already in the closed list
            inClosedList = False
            for closedNode in closedList:
                if child.position == closedNode.position:
                    inClosedList = True
                    break

            # Check if the child node is already in the open list
            inOpenList = False
            for openNode in openList:
                if child.position == openNode.position:
                    inOpenList = True
                    break

            # Add the child node to the open list if it's not already in the open or closed list
            if not inClosedList and not inOpenList:
                openList.append(child)

    # If the open list is empty and the end node is not found, return None
    return None
# def A_Star(map, startNode, endNode, children = []):
#     currentNode = startNode

#     #Đánh dấu các điểm đã đi qua bằng giá trị 3
#     map[currentNode.position[0]][currentNode.position[1]] = 3

#     #Kiểm tra nếu vị trí node hiện tại bằng vị trí đích thì trả về node hiện tại
#     if currentNode.position[0] == endNode.position[0] and currentNode.position[0] == endNode.position[0]:
#         return currentNode
    
#     #Kiểm tra các vị trí có thể di chuyển của node hiện tại
#     for move in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
#         move_to = (currentNode.position[0] + move[0], currentNode.position[1] + move[1])
#         #Kiểm tra vị trí cớ hợp lệ không và đã duyệt qua hay chưa, nêu hợp lệ thì tạo node con và đánh dấu giá trị 2
#         if move_to[0] >= 0 and move_to[0] <= 9 and move_to[1] >= 0 and move_to[1] <= 9 and map[move_to[0]][move_to[1]] == 0:
#             map[move_to[0]][move_to[1]] = 2
#             childNode = Node(currentNode, move_to)
#             children.append(childNode)
    
#     '''Sử dựng Diagonal distance heuristic
#         Tham khảo tại http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html#:~:text=Diagonal%20distance%23,the%20cost%20of%20moving%20diagonally.'''
#     for child in children:
#         #Đi ngang hoặc dọc tốn cost là 1, đi chéo tốn cost là sqrt(2)
#         child.g = currentNode.g + math.sqrt((child.parent.position[0] - child.position[0])**2 + (child.parent.position[1] - child.position[1])**2)

#         #Gom lại từ công thức (dx+dy) + sqrt(2)*min(dx,dy) - 2*min(dx,dy)
#         #Trong đó:
#         #   dx+dy là số bước phải đi nếu không theo đường chéo
#         #   sqrt(2)*min(dx,dy) là số bước đường chéo có thể đi
#         #   2*min(dx,dy) là số bước tiết kiệm được, 1 đường chéo tiết kiệm được 2 cạnh thẳng
#         dx = abs(child.position[0] - endNode.position[0])
#         dy = abs(child.position[1] - endNode.position[1])
#         child.h = (dx + dy) + (math.sqrt(2) - 2) * min(dx, dy)

#         child.f = child.g + child.h
    
#     #Tìm node con có f nhỏ nhất
#     childMin = children[0]
#     for child in children:
#         if(childMin.f > child.f):
#             childMin = child
#     children.remove(childMin)
    
#     #Gọi đệ quy, cho node con có f nhỏ nhất để tiếp tục duyệt
#     return (A_Star(map, childMin, endNode, children))


# map = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
#        [0, 1, 0, 0, 0, 1, 1, 1, 1, 0],
#        [0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
#        [0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
#        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
#        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
#        [0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
#        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
#        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0]]

# start = Node(None, (0, 0))
# end = Node(None, (8, 9))
# answer = A_Star(map, start, end)

# #Tạo một list để chứa đường dẫn, bắt đầu từ node ở đích hiện tại
# path = [answer.position]
# #Truy ngược về node cha để thêm vào đường dẫn
# while answer.parent != None:
#     path.append(answer.parent.position)
#     answer = answer.parent
# #Đảo ngược đường dẫn về đúng thứ tự từ bắt đầu đến kết thúc

# path.pop()
# path.reverse()
# print(path)


    

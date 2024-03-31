import math
import random

class GameObject:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy


class Wall(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)


class Obstacle(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)


class Agent(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)


class Hider(Agent):
    def __init__(self, x, y):
        super().__init__(x, y)


class Seeker(Agent):
    def __init__(self, x, y):
        super().__init__(x, y)


class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(width)] for _ in range(height)]

    def add_object(self, obj):
        self.grid[obj.y][obj.x] = obj

    def remove_object(self, obj):
        self.grid[obj.y][obj.x] = None

    def move_agent(self, agent, dx, dy):
        if 0 <= agent.x + dx < self.width and 0 <= agent.y + dy < self.height:
            if self.grid[agent.y + dy][agent.x + dx] is None:
                self.remove_object(agent)
                agent.move(dx, dy)
                self.add_object(agent)
                return True
        return False


class HideAndSeekGame:
    def __init__(self, width, height, max_steps):
        self.map = GameMap(width, height)
        self.hider = Hider(0, 0)  # Tạm thời đặt hider ở (0, 0)
        self.seeker = Seeker(width - 1, height - 1)  # Tạm thời đặt seeker ở (width - 1, height - 1)
        self.max_steps = max_steps
        self.steps_taken = 0
        self.map.add_object(self.hider)
        self.map.add_object(self.seeker)
        self.hide_mark = False
        self.hide_mark_radius = 2

    def move_hider(self, dx, dy):
        return self.map.move_agent(self.hider, dx, dy)

    def move_seeker(self, dx, dy):
        self.steps_taken += 1
        if self.can_move(self.seeker, dx, dy):
            return self.map.move_agent(self.seeker, dx, dy)
        else:
            return False

    def can_move(self, agent, dx, dy):
        new_x = agent.x + dx
        new_y = agent.y + dy
        if not (0 <= new_x < self.map.width and 0 <= new_y < self.map.height):
            return False
        if isinstance(self.map.grid[new_y][new_x], Wall) or isinstance(self.map.grid[new_y][new_x], Obstacle):
            return False
        return True

    def check_game_over(self):
        if abs(self.hider.x - self.seeker.x) <= 1 and abs(self.hider.y - self.seeker.y) <= 1:
            return "Seeker found the hider!"
        elif self.steps_taken >= self.max_steps:
            return "Max steps reached. Game over!"
        return None

    def seeker_vision(self):
        vision_range = 3
        seeker_x, seeker_y = self.seeker.x, self.seeker.y
        for y in range(seeker_y - vision_range, seeker_y + vision_range + 1):
            for x in range(seeker_x - vision_range, seeker_x + vision_range + 1):
                if 0 <= x < self.map.width and 0 <= y < self.map.height:
                    if abs(x - seeker_x) + abs(y - seeker_y) <= vision_range:
                        if self.map.grid[y][x] is None or isinstance(self.map.grid[y][x], Hider):
                            print(".", end=" ")  # Replace this with any visualization you prefer
                        else:
                            print("X", end=" ")  # Replace this with any visualization you prefer
                    else:
                        print("#", end=" ")  # Replace this with any visualization you prefer
                else:
                    print("#", end=" ")  # Replace this with any visualization you prefer
            print()

    def hider_action(self):
        if self.steps_taken >= 5 and not self.hide_mark:
            self.hide_mark = True
            self.mark_hider_surroundings()

    def mark_hider_surroundings(self):
        for dx in range(-self.hide_mark_radius, self.hide_mark_radius + 1):
            for dy in range(-self.hide_mark_radius, self.hide_mark_radius + 1):
                if 0 <= self.hider.x + dx < self.map.width and 0 <= self.hider.y + dy < self.map.height:
                    if self.map.grid[self.hider.y + dy][self.hider.x + dx] is None:
                        self.map.grid[self.hider.y + dy][self.hider.x + dx] = Obstacle(self.hider.x + dx, self.hider.y + dy)


################################################################################



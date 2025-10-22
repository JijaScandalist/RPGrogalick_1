import math
from settings import *

class Fireball:
    def __init__(self, x, y, angle, speed=8):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.alive = True

    def update(self, world_map):
        # движение
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)

        # проверка столкновения со стенами
        map_x, map_y = int(self.x // tile * tile), int(self.y // tile * tile)
        if (map_x, map_y) in world_map:
            self.alive = False

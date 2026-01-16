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

    def update(self, world_map, enemies=None):
        """Обновление файрбола"""
        # движение
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)

        # проверка столкновения со стенами
        map_x, map_y = int(self.x // tile * tile), int(self.y // tile * tile)
        if (map_x, map_y) in world_map:
            self.alive = False

        # НОВОЕ: проверка столкновения с врагами
        if enemies:
            for enemy in enemies:
                if not enemy.alive:
                    continue
                dx = self.x - enemy.x
                dy = self.y - enemy.y
                distance = math.sqrt(dx * dx + dy * dy)
                if distance < 30:  # Радиус попадания
                    enemy.take_damage(34)  # Урон от файрбола
                    self.alive = False
                    break

    # И в player.py обновите метод update_fireballs:
    def update_fireballs(self, enemies):
        for fireball in self.fireballs[:]:
            fireball.update(world_map, enemies)
            if not fireball.alive:
                self.fireballs.remove(fireball)

    # В main.py измените вызов:
    #player.update_fireballs(enemies)

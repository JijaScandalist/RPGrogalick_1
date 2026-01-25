import pygame
import math
from settings import *
from map import world_map
from sprites import Enemy, Slime


class Fireball:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 10
        self.radius = 5
        self.alive = True
        self.damage = 30
        self.lifetime = 100  # Количество кадров до исчезновения

    def update(self, world_map, enemies):
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.alive = False
            return

        # Движение
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)

        # Проверка столкновений со стенами
        map_x = int(self.x // tile) * tile
        map_y = int(self.y // tile) * tile
        if (map_x, map_y) in world_map:
            self.alive = False
            return

        # Проверка столкновений с врагами
        for enemy in enemies:
            if not enemy.alive:
                continue

            dx = self.x - enemy.x
            dy = self.y - enemy.y
            distance = math.sqrt(dx * dx + dy * dy)

            if distance < self.radius + 30:  # 30 - примерный радиус врага
                enemy.take_damage(self.damage)
                self.alive = False
                return
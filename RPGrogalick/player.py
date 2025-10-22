#управление
import sys

from settings import *
import pygame
import math
from equipment import Fireball
from map import world_map

class Player:
    def __init__(self):
        self.x, self.y = player_position
        self.angle = player_angle
        self.ver_a = player_ver_angle
        self.delta = 0
        self.fireballs = []

    @property #возврат позиции по х и у
    def position(self):
        return (self.x, self.y)

    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.x += player_speed * cos_a
            self.y += player_speed * sin_a
            #print('W')
        if keys[pygame.K_s]:
            self.x += -player_speed * cos_a
            self.y += -player_speed * sin_a
            #print('S')
        if keys[pygame.K_a]:
            self.x += player_speed * sin_a
            self.y += -player_speed * cos_a
            #print('A')
        if keys[pygame.K_d]:
            self.x += -player_speed * sin_a
            self.y += player_speed * cos_a
            #print('D')

        # if keys[pygame.K_LEFT]:
        #     self.angle -= 0.1
        # if keys[pygame.K_RIGHT]:
        #     self.angle += 0.1
        # if keys[pygame.K_UP]:
        #     self.ver_a -= 10
        # if keys[pygame.K_DOWN]:
        #     self.ver_a += 10
        self.mouse_control()

        if keys[pygame.K_SPACE]:
            self.shoot()
        if keys[pygame.K_ESCAPE]:
            sys.exit()

    def mouse_control(self):
        if pygame.mouse.get_focused():
            difference = pygame.mouse.get_pos()[0] - half_width
            pygame.mouse.set_pos(half_width, half_height)
            self.angle += difference * 0.015

    def shoot(self):
        #  новый снаряд
        offset_x = math.cos(self.angle) * 20
        offset_y = math.sin(self.angle) * 20
        fireball = Fireball(self.x + offset_x, self.y + offset_y, self.angle)
        self.fireballs.append(fireball)

    def update_fireballs(self):
        # обновление всех активные снаряды
        for fireball in self.fireballs[:]:
            fireball.update(world_map)
            if not fireball.alive:
                self.fireballs.remove(fireball)
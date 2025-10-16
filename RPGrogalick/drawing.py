import math

import pygame
from settings import *
from ray_casting import ray_casting
from map import mini_map

class Drawing:
    def __init__(self, sc, sc_map):
        self.sc = sc
        self.sc_map = sc_map
        self.font = pygame.font.SysFont('Arial', 36, bold=True)
        self.textures = {'1': pygame.image.load("image/388673.jpg").convert(),
                         '2': pygame.image.load("image/owl_1.jpg").convert(),
                         '3': pygame.image.load("image/pngtree-mystery-forest-with-big-dark-green-pine-trees-picture-image_2049712.jpg").convert(),
                         'S': pygame.image.load("image/sky_1.jpg").convert(),
                         }

    def background(self, angle):
        # пол и потолок
        # pygame.draw.rect(self.sc, skyblue, (0, 0, width, half_height))
        sky_offset = -5 * math.degrees(angle) % width
        self.sc.blit(self.textures['S'], (sky_offset, 0))
        self.sc.blit(self.textures['S'], (sky_offset - width, 0))
        self.sc.blit(self.textures['S'], (sky_offset + width, 0))
        pygame.draw.rect(self.sc, dark_green, (0, half_height, width, half_height))

    #рекаст
    def world(self, player_position, player_angle):
        ray_casting(self.sc, player_position, player_angle, self.textures)

    def fps(self, clock):
        display_fps = str(int(clock.get_fps()))
        render = self.font.render(display_fps, 0, red)
        self.sc.blit(render, fps_pos)
    def mini_map(self, player):
        self.sc_map.fill(black)
        map_x, map_y = player.x // map_scale, player.y // map_scale
        pygame.draw.line(self.sc_map, purple, (map_x, map_y),
                         (map_x + 12 * math.cos(player.angle), map_y + 12 * math.sin(player.angle)))
        pygame.draw.circle(self.sc_map, red, (int(map_x), int(map_y)), 5)
        for x, y in mini_map:
            pygame.draw.rect(self.sc_map, sandy, (x, y, map_tile, map_tile))
        self.sc.blit(self.sc_map, map_pos)
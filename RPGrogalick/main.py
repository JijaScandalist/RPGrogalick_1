import pygame
from settings import *
from player import Player
import math
from map import world_map
from ray_casting import ray_casting
from drawing import Drawing

pygame.init()
sc = pygame.display.set_mode((width, height))
sc_map = pygame.Surface((width // map_scale, height // map_scale))
clock = pygame.time.Clock() #fps
player = Player()
drawing = Drawing(sc, sc_map)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    player.movement()
    sc.fill(black) #закраска поверхности

    #пол и потолок
    # pygame.draw.rect(sc, skyblue, (0, 0, width, half_height))
    # pygame.draw.rect(sc, dark_green, (0, half_height, width, half_height))
    drawing.background(player.angle)
    drawing.world(player.position, player.angle)
    drawing.fps(clock)
    drawing.mini_map(player)

    # pygame.draw.circle(sc, green, (int(player.x), int(player.y)), 12)
    # pygame.draw.line(sc, blue, player.position, (player.x + width * math.cos(player.angle), player.y + height * math.sin(player.angle)))
    # for x, y in world_map:
    #     pygame.draw.rect(sc, red, (x, y, tile, tile), 2)

    pygame.display.flip()
    clock.tick(fps)




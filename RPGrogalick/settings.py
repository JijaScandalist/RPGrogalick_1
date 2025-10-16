#game settings
import pygame
from random import randint
import math

#каритинки/текстуры
image_1 = pygame.image.load("image/388673.jpg")

#шрифт
#myfont = pygame.font.Font("fonts/BebasNeue-Regular.ttf")

#main
width = 1200
height = 800
half_width = width // 2
half_height = height // 2
fps = 60
tile = 100
fps_pos = (width - 65, 5)

#colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
dark_green = (0, 128, 0)
blue = (0, 0, 255)
darkgray = (128, 128, 128)
purple = (128, 0, 128)
yellow = (255, 255, 0)
cyan = (0, 255, 255)
magenta = (255, 0, 255)
skyblue = (0, 128, 255)
sandy = (144, 164, 96)
def color_r(): #рандомный цвет (на всякий случай)
    return (randint(0, 255), randint(0, 255), randint(0, 255))

#player settings
player_position = (half_width, half_height)
player_angle = 0
player_speed = 2

#rays
fov = math.pi / 3
half_fov = fov / 2
num_rays = 300
max_depth = 800
delta_angle = fov / num_rays
dist = num_rays / (2 * math.tan(half_fov))
proj_coef = 3 * dist * tile
scale = width // num_rays

#minimap settings
map_scale = 5
map_tile = tile // map_scale
map_pos = (0, height - height // map_scale)

#texture (1200x1200)
texture_width = 1200
texture_height = 1200
texture_scale = texture_width // tile

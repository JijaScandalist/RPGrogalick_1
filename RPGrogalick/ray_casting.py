import pygame
from settings import *
from map import world_map

#функция принимает поверхность отрисовки, позицию и угол игрока
# def ray_casting(sc, player_position, player_angle):
#     cur_angle = player_angle - half_fov
#     xo, yo = player_position
#     for ray in range(num_rays):
#         sin_a = math.sin(cur_angle)
#         cos_a = math.cos(cur_angle)
#         for depth in range(max_depth):
#             x = xo + depth * cos_a
#             y = yo + depth * sin_a
#             #pygame.draw.line(sc, darkgray, player_position, (x, y), 2)
#             if (x // tile * tile, y // tile * tile) in world_map:
#                 #убрать эффект рыб глаза
#                 depth *= math.cos(player_angle - cur_angle)
#                 proj_height = proj_coef / depth
#                 #глубина поверхностей
#                 c = 255 // (1 + depth * depth * 0.00002)
#                 color = (c, c // 2, c // 3)
#
#                 # c_1 = 128 // (1 + depth * depth * 0.0001)
#                 # color_1 = (c_1, c_1, c_1)
#
#                 pygame.draw.rect(sc, color, (ray * scale, half_height - proj_height // 2, scale, proj_height))
#                 break
#         cur_angle += delta_angle

def mapping(a, b):
    return (a // tile) * tile, (b // tile) * tile

def ray_casting(sc, player_position, player_angle, textures):
    ox, oy = player_position
    xm, ym = (ox // tile) * tile, (oy // tile) * tile
    cur_angle = player_angle - half_fov
    for ray in range(num_rays):
        sin_a = math.sin(cur_angle)
        cos_a = math.cos(cur_angle)

        #verticals
        # if cos >= 0:
        #     x = xm + tile
        #     dx = 1
        # else:
        #     x = xm
        #     dx = -1

        x, dx = (xm + tile, 1) if cos_a >= 0 else (xm, -1)
        #все вертикали в цикле
        for i in range(0, width, tile):
            depth_v = (x - ox) / cos_a
            yv = oy + depth_v * sin_a
            tile_v = mapping (x + dx, yv)
            if tile_v in world_map:
                texture_v = world_map[tile_v]
                break
            x += dx * tile

        #пересечение с горизонтальными отрезками
        y, dy = (ym + tile, 1) if sin_a >= 0 else (ym, -1)
        for i in range(0, height, tile):
            depth_h = (y - oy) / sin_a
            xh = ox + depth_h * cos_a
            tile_h = mapping(xh, y + dy)
            if tile_h in world_map:
                texture_h = world_map[tile_h]
                break
            y += dy * tile

        #projection
        depth, offset, texture = (depth_v, yv, texture_v) if depth_v < depth_h else (depth_h, xh, texture_h)
        offset = int(offset) % tile
        #убрать эффект рыб глаза
        depth *= math.cos(player_angle - cur_angle)
        depth = max(depth, 0.00001)
        #proj_height = proj_coef // depth
        proj_height = min(int(proj_coef / depth), 2 * height)

        #глубина поверхностей
        # c = 255 // (1 + depth * depth * 0.00002)
        # color = (c, c // 2, c // 3)
        #
        # # c_1 = 128 // (1 + depth * depth * 0.0001)
        # # color_1 = (c_1, c_1, c_1)
        #
        # pygame.draw.rect(sc, color, (ray * scale, half_height - proj_height // 2, scale, proj_height))

        wall_column = textures[texture].subsurface(offset * texture_scale, 0, texture_scale, texture_height)
        wall_column = pygame.transform.scale(wall_column, (scale, proj_height))
        sc.blit(wall_column, (ray * scale, half_height - proj_height // 2))

        cur_angle += delta_angle


#ray_casting

import pygame
from settings import *
from map import world_map, floor_map, ceiling_map
from player import *
import math


def mapping(a, b):
    return (a // tile) * tile, (b // tile) * tile


def ray_casting(sc, player_position, player_angle, textures, player_pitch=0):
    global texture_v, texture_h
    ox, oy = player_position
    xm, ym = (ox // tile) * tile, (oy // tile) * tile
    cur_angle = player_angle - half_fov

    for ray in range(num_rays):
        sin_a = math.sin(cur_angle)
        cos_a = math.cos(cur_angle)

        # Кешируем коррекцию рыбьего глаза для оптимизации
        cos_correction = math.cos(player_angle - cur_angle)

        # verticals
        x, dx = (xm + tile, 1) if cos_a >= 0 else (xm, -1)
        foended = False

        # все вертикали в цикле
        for i in range(0, width, tile):
            depth_v = (x - ox) / cos_a
            yv = oy + depth_v * sin_a
            tile_v = mapping(x + dx, yv)
            if tile_v in world_map:
                texture_v = world_map[tile_v]
                foended = True
                break
            x += dx * tile

        # пересечение с горизонтальными отрезками
        y, dy = (ym + tile, 1) if sin_a >= 0 else (ym, -1)
        for i in range(0, height, tile):
            depth_h = (y - oy) / sin_a
            xh = ox + depth_h * cos_a
            tile_h = mapping(xh, y + dy)
            if tile_h in world_map:
                texture_h = world_map[tile_h]
                foended = True
                break
            y += dy * tile

        if foended:
            # projection
            depth, offset, texture = (depth_h, xh, texture_h) if depth_v >= depth_h else (depth_v, yv, texture_v)
            offset = int(offset) % tile

            # убрать эффект рыбьего глаза
            depth *= math.cos(player_angle - cur_angle)
            depth = max(depth, 0.00001)

            proj_height = min(int(proj_coef / depth), 2 * height)

            # Отрисовка стены с учётом pitch (вертикального угла)
            wall_column = textures[texture].subsurface(offset * texture_scale, 0, texture_scale, texture_height)
            wall_column = pygame.transform.scale(wall_column, (scale, proj_height))

            # Смещение по вертикали в зависимости от pitch
            pitch_offset = int(player_pitch * 200)
            wall_pos_y = half_height - proj_height // 2 + pitch_offset

            sc.blit(wall_column, (ray * scale, wall_pos_y))

            # FLOORCASTING 
            #  пол и потолок смещаются с pitch
            floor_start = wall_pos_y + proj_height
            ceiling_end = wall_pos_y

            # Шаг для оптимизации
            step = 3

            # FLOOR - ОПТИМИЗИРОВАНО
            for y in range(floor_start, height, step):
                if y <= half_height + pitch_offset:
                    continue

                # Расстояние до точки на полу с учетом pitch
                row_distance = (player_height * dist) / (y - half_height - pitch_offset)
                straight_dist = row_distance / cos_correction

                # Мировые координаты
                floor_x = ox + straight_dist * cos_a
                floor_y = oy + straight_dist * sin_a

                # Определяем плитку из floor_map (как у стен)
                floor_tile_pos = mapping(floor_x, floor_y)

                # Проверяем, есть ли плитка пола на этой позиции
                if floor_tile_pos in floor_map:
                    floor_texture_key = floor_map[floor_tile_pos]

                    if floor_texture_key in textures:
                        # Координаты внутри плитки
                        tx = int(floor_x) % tile
                        ty = int(floor_y) % tile

                        # Координаты в текстуре - упрощено
                        texture_x = min((tx * texture_scale) // tile, texture_width - 1)
                        texture_y = min((ty * texture_scale) // tile, texture_height - 1)

                        # Получаем цвет напрямую
                        floor_color = textures[floor_texture_key].get_at((texture_x, texture_y))

                        # Упрощённое затемнение
                        shade = max(0.3, 1.0 - straight_dist * 0.00150)
                        color = (
                            int(floor_color[0] * shade),
                            int(floor_color[1] * shade),
                            int(floor_color[2] * shade)
                        )

                        pygame.draw.rect(sc, color, (ray * scale, y, scale, step))
                    else:
                        pygame.draw.rect(sc, (40, 60, 40), (ray * scale, y, scale, step))

            # CEILING 
            for y in range(0, ceiling_end, step):
                if y >= half_height + pitch_offset:
                    continue

                # Расстояние до точки на потолке с учетом pitch
                row_distance = (player_height * dist) / (half_height + pitch_offset - y)
                straight_dist = row_distance / cos_correction

                ceiling_x = ox + straight_dist * cos_a
                ceiling_y = oy + straight_dist * sin_a

                ceiling_tile_pos = mapping(ceiling_x, ceiling_y)

                if ceiling_tile_pos in ceiling_map:
                    ceiling_texture_key = ceiling_map[ceiling_tile_pos]

                    if ceiling_texture_key in textures:
                        tx = int(ceiling_x) % tile
                        ty = int(ceiling_y) % tile

                        texture_x = min((tx * texture_scale) // tile, texture_width - 1)
                        texture_y = min((ty * texture_scale) // tile, texture_height - 1)

                        ceiling_color = textures[ceiling_texture_key].get_at((texture_x, texture_y))
                        shade = max(0.2, 0.7 - straight_dist * 0.00125)
                        color = (
                            int(ceiling_color[0] * shade),
                            int(ceiling_color[1] * shade),
                            int(ceiling_color[2] * shade)
                        )

                        pygame.draw.rect(sc, color, (ray * scale, y, scale, step))

        cur_angle += delta_angle


def ray_casting_for_sprite(player_pos, sprite_pos, player_angle, world_map):
    """Проверяет, виден ли спрайт (нет ли стен между игроком и спрайтом)"""
    ox, oy = player_pos
    sx, sy = sprite_pos

    dx = sx - ox
    dy = sy - oy
    distance = math.sqrt(dx * dx + dy * dy)

    if distance < 1:
        return True

    # Направление луча
    steps = int(distance / 10)  # Проверяем каждые 10 пикселей
    step_x = dx / steps
    step_y = dy / steps

    # Идём по лучу и проверяем стены
    for i in range(steps):
        check_x = ox + step_x * i
        check_y = oy + step_y * i

        if mapping(check_x, check_y) in world_map:
            return False  # Стена блокирует обзор

    return True  # Путь чист

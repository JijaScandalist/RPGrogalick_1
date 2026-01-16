#drawing

import math
import pygame
from settings import *
from ray_casting import ray_casting
from map import mini_map
from player import *


class Drawing:
    def __init__(self, sc, sc_map):
        self.sc = sc
        self.sc_map = sc_map
        self.font = pygame.font.SysFont('Arial', 36, bold=True)

        # текстуры
        self.textures = {
            '1': pygame.image.load("image/388673.jpg").convert(),
            '2': pygame.image.load("image/owl_1.jpg").convert(),
            '3': pygame.image.load(
                "image/pngtree-mystery-forest-with-big-dark-green-pine-trees-picture-image_2049712.jpg").convert(),
            'S': pygame.image.load("image/sky_1.jpg").convert(),
            'T': pygame.image.load("image/trava_1.png").convert(),

            'R': self.create_color_texture(color_r()),

            # ТЕКСТУРЫ ПОЛА (добавьте свои)
            'floor1': pygame.image.load("image/plitka2.jpg").convert(),
            'floor2': pygame.image.load("image/plitka.jpg").convert(),
            'floor3': pygame.image.load("image/plitka3.jpg").convert(),
            'floor4': pygame.image.load("image/lava_1.jpg").convert(),
            'floor5': pygame.image.load("image/lava_2.jpg").convert(),

            # ТЕКСТУРЫ ПОТОЛКА (опционально)
            'ceiling1': pygame.image.load("image/trava_1.png").convert(),
            'ceiling2': pygame.image.load("image/trava_1.png").convert(),

            # СЛИЗНИ - БОЛЬШИЕ
            'slime_large_front': pygame.image.load("sprites_txt/slime-move-0.png").convert_alpha(),
            'slime_large_back': pygame.image.load("sprites_txt/slime-move-1.png").convert_alpha(),
            'slime_large_left': pygame.image.load("sprites_txt/slime-move-2.png").convert_alpha(),
            'slime_large_right': pygame.image.load("sprites_txt/slime-move-3.png").convert_alpha(),

            # СЛИЗНИ - СРЕДНИЕ
            'slime_medium_front': pygame.image.load("sprites_txt/slime-move-0.png").convert_alpha(),
            'slime_medium_back': pygame.image.load("sprites_txt/slime-move-1.png").convert_alpha(),
            'slime_medium_left': pygame.image.load("sprites_txt/slime-move-2.png").convert_alpha(),
            'slime_medium_right': pygame.image.load("sprites_txt/slime-move-3.png").convert_alpha(),

            # СЛИЗНИ - МАЛЕНЬКИЕ
            'slime_small_front': pygame.image.load("sprites_txt/slime-move-0.png").convert_alpha(),
            'slime_small_back': pygame.image.load("sprites_txt/slime-move-1.png").convert_alpha(),
            'slime_small_left': pygame.image.load("sprites_txt/slime-move-2.png").convert_alpha(),
            'slime_small_right': pygame.image.load("sprites_txt/slime-move-3.png").convert_alpha(),

            # Если нет всех текстур
            # 'enemy_front': pygame.image.load("image/enemy.png").convert_alpha(),
            # И в других: self.textures['enemy_back'] = self.textures['enemy_front']

            # МЕЧ
            'sword': pygame.image.load("sprites_txt/woodcutter axe.png").convert_alpha(),

            # ПРИЦЕЛ
            'crosshair': self.create_crosshair()
        }

        # Анимация меча
        self.sword_animation = 0
        self.is_attacking = False

    def create_color_texture(self, color):
        #создает цвет как текстуру
        surface = pygame.Surface((texture_width, texture_height))
        surface.fill(color)
        return surface.convert()


    def background(self, angle):
        # Небо
        sky_offset = -5 * math.degrees(angle) % width
        self.sc.blit(self.textures['S'], (sky_offset, 0))
        self.sc.blit(self.textures['S'], (sky_offset - width, 0))
        self.sc.blit(self.textures['S'], (sky_offset + width, 0))

        
        # pygame.draw.rect(self.sc, dark_green, (0, half_height, width, half_height))
    
    def world(self, player):
        ray_casting(self.sc, player.position, player.angle, self.textures, player.pitch)

    def fps(self, clock):
        display_fps = str(int(clock.get_fps()))
        render = self.font.render(display_fps, 0, red)
        self.sc.blit(render, fps_pos)

    def health(self, ps_health):
        bar_width = 200
        bar_height = 40
        fill_width = (ps_health / 100) * bar_width
        # Рамка (черная, ширина 2)
        pygame.draw.rect(self.sc, black, (8, 8, bar_width + 4, bar_height + 4), 5)
        # Фон шкалы (серый)
        pygame.draw.rect(self.sc, darkgray, (10, 10, bar_width, bar_height))
        # Заполнение зеленым
        pygame.draw.rect(self.sc, green, (10, 10, fill_width, bar_height))
        # Опционально: текст с текущим здоровьем
        render = self.font.render(f"{int(ps_health)}", 0, white)
        self.sc.blit(render, (10 + bar_width // 2 - 20, 10))

    def mini_map(self, player):
        self.sc_map.fill(black)
        map_x, map_y = player.x // map_scale, player.y // map_scale
        pygame.draw.line(self.sc_map, purple, (map_x, map_y),
                         (map_x + 12 * math.cos(player.angle), map_y + 12 * math.sin(player.angle)))
        pygame.draw.circle(self.sc_map, red, (int(map_x), int(map_y)), 5)
        for x, y in mini_map:
            pygame.draw.rect(self.sc_map, sandy, (x, y, map_tile, map_tile))
        self.sc.blit(self.sc_map, map_pos)

    def fireballs(self, player):
        for fireball in player.fireballs:
            fire_img = pygame.image.load("image/fireball.jpg").convert_alpha()
            rect = fire_img.get_rect(center=(int(fireball.x), int(fireball.y)))
            self.sc.blit(fire_img, rect)

    def create_crosshair(self):
        """Создаёт прицел"""
        size = 32
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        center = size // 2

        # Крестик
        pygame.draw.line(surface, (255, 255, 255), (center - 10, center), (center - 3, center), 2)
        pygame.draw.line(surface, (255, 255, 255), (center + 3, center), (center + 10, center), 2)
        pygame.draw.line(surface, (255, 255, 255), (center, center - 10), (center, center - 3), 2)
        pygame.draw.line(surface, (255, 255, 255), (center, center + 3), (center, center + 10), 2)

        # Обводка для контраста
        pygame.draw.line(surface, (0, 0, 0), (center - 10, center), (center - 3, center), 3)
        pygame.draw.line(surface, (0, 0, 0), (center + 3, center), (center + 10, center), 3)
        pygame.draw.line(surface, (0, 0, 0), (center, center - 10), (center, center - 3), 3)
        pygame.draw.line(surface, (0, 0, 0), (center, center + 3), (center, center + 10), 3)

        return surface

    def sprites(self, player, sprite_list):
        """Отрисовка спрайтов с проверкой видимости"""
        from ray_casting import ray_casting_for_sprite
        from map import world_map

        sprite_data = []
        for sprite in sprite_list:
            if not sprite.alive:
                continue

            # Проверяем, не закрыт ли спрайт стеной
            if not ray_casting_for_sprite(player.position, sprite.position, player.angle, world_map):
                continue

            projection = sprite.get_sprite_projection(
                player.position,
                player.angle,
                player.pitch
            )

            if projection:
                sprite_data.append((projection, sprite))

        # Сортируем по расстоянию
        sprite_data.sort(key=lambda x: x[0]['distance'], reverse=True)

        # Отрисовываем
        for projection, sprite in sprite_data:
            texture_key = projection['texture_key']

            # Получаем текстуру
            if texture_key in sprite.textures:
                texture = sprite.textures[texture_key]
            else:
                texture = sprite.textures.get('front', list(sprite.textures.values())[0])

            #  используем NEAREST для пикселизации
            scaled_sprite = pygame.transform.scale(
                texture,
                (projection['sprite_width'], projection['sprite_height'])
            )

            # Позиция с учётом pitch
            sprite_x = projection['screen_x'] - projection['sprite_width'] // 2
            sprite_y = half_height - projection['sprite_height'] // 2 + projection['pitch_offset']

            # затемнение
            distance = projection['distance']
            shade = max(0.2, 1.0 - distance * 0.0015)

            # Применяем затемнение
            dark_sprite = scaled_sprite.copy()
            dark_sprite.fill(
                (int(255 * shade), int(255 * shade), int(255 * shade)),
                special_flags=pygame.BLEND_RGB_MULT
            )

            self.sc.blit(dark_sprite, (sprite_x, sprite_y))

            
            if distance < 200:  # Показываем только для близких врагов
                debug_font = pygame.font.SysFont('Arial', 16)
                dist_text = debug_font.render(f"{int(distance)}px", True, (255, 255, 0))
                self.sc.blit(dist_text, (sprite_x, sprite_y - 20))

    def weapon(self, is_attacking):
        """Отрисовка меча"""
        sword_texture = self.textures['sword']

        # Анимация атаки
        if is_attacking:
            self.sword_animation = min(self.sword_animation + 5, 30)
        else:
            self.sword_animation = max(self.sword_animation - 3, 0)

        # Размер и позиция меча
        sword_width = 400
        sword_height = 400

        # Смещение при атаке
        offset_y = -self.sword_animation * 3
        rotation = -self.sword_animation

        # Масштабируем и поворачиваем
        scaled_sword = pygame.transform.scale(sword_texture, (sword_width, sword_height))
        rotated_sword = pygame.transform.rotate(scaled_sword, rotation)

        # Позиция (справа внизу)
        sword_x = width - sword_width + 100
        sword_y = height - sword_height + 150 + offset_y

        self.sc.blit(rotated_sword, (sword_x, sword_y))

    def crosshair(self):
        """Отрисовка прицела"""
        crosshair_texture = self.textures['crosshair']
        crosshair_x = half_width - 16
        crosshair_y = half_height - 16
        self.sc.blit(crosshair_texture, (crosshair_x, crosshair_y))




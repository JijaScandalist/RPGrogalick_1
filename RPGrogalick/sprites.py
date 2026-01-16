import pygame
import math
from settings import *
from ray_casting import ray_casting_for_sprite


class Sprite:
    def __init__(self, x, y, textures_dict, scale_factor=0.8):
        self.x = x
        self.y = y
        self.textures = textures_dict  # Словарь с текстурами для разных углов
        self.scale_factor = scale_factor
        self.alive = True
        self.health = 100

    @property
    def position(self):
        return (self.x, self.y)

    def get_texture_by_angle(self, player_pos, player_angle):
        """Определяет какую текстуру показать в зависимости от угла обзора"""
        dx = self.x - player_pos[0]
        dy = self.y - player_pos[1]

        # Угол ОТ спрайта К игроку (что видит спрайт)
        sprite_to_player = math.atan2(-dy, -dx)

        # Разница между направлением спрайта на игрока и направлением взгляда игрока
        # Это покажет с какой стороны игрок смотрит на спрайт
        angle_diff = player_angle - sprite_to_player

        # Нормализуем угол
        while angle_diff > math.pi:
            angle_diff -= 2 * math.pi
        while angle_diff < -math.pi:
            angle_diff += 2 * math.pi

        # Конвертируем в градусы для удобства
        angle_deg = math.degrees(angle_diff)

        # Определяем направление (8 направлений)
        # front = игрок видит лицо врага
        # back = игрок видит спину врага
        if -22.5 <= angle_deg < 22.5:
            return 'front'  # Лицом к игроку
        elif 22.5 <= angle_deg < 67.5:
            return 'front_left'
        elif 67.5 <= angle_deg < 112.5:
            return 'left'
        elif 112.5 <= angle_deg < 157.5:
            return 'back_left'
        elif 157.5 <= angle_deg <= 180 or -180 <= angle_deg < -157.5:
            return 'back'  # Спиной к игроку
        elif -157.5 <= angle_deg < -112.5:
            return 'back_right'
        elif -112.5 <= angle_deg < -67.5:
            return 'right'
        else:  # -67.5 <= angle_deg < -22.5
            return 'front_right'

    def get_sprite_projection(self, player_pos, player_angle, player_pitch):
        """Вычисляет параметры для отрисовки спрайта с учетом pitch"""
        dx = self.x - player_pos[0]
        dy = self.y - player_pos[1]

        # Расстояние до спрайта
        distance = math.sqrt(dx * dx + dy * dy)
        if distance < 0.1:
            return None

        # Угол к спрайту
        sprite_angle = math.atan2(dy, dx)

        # Разница углов
        angle_diff = sprite_angle - player_angle

        # Нормализуем
        while angle_diff > math.pi:
            angle_diff -= 2 * math.pi
        while angle_diff < -math.pi:
            angle_diff += 2 * math.pi

        # Проверяем видимость
        if abs(angle_diff) > half_fov:
            return None

        # Вычисляем позицию на экране
        screen_x = (half_fov + angle_diff) / fov * num_rays

        # Размер спрайта
        sprite_height = min(int(proj_coef / distance * self.scale_factor), 2 * height)
        sprite_width = sprite_height

        # Определяем текстуру по углу обзора
        texture_key = self.get_texture_by_angle(player_pos, player_angle)

        # Смещение по вертикали от pitch
        pitch_offset = int(player_pitch * 200)

        return {
            'screen_x': int(screen_x * scale),
            'distance': distance,
            'sprite_height': sprite_height,
            'sprite_width': sprite_width,
            'texture_key': texture_key,
            'pitch_offset': pitch_offset
        }


class Enemy(Sprite):
    def __init__(self, x, y, textures_dict, scale_factor=0.8):
        super().__init__(x, y, textures_dict, scale_factor)
        self.speed = 1.5
        self.attack_range = 80
        self.attack_damage = 10
        self.attack_cooldown = 0

    def update(self, player_pos, world_map):
        """Обновление AI врага"""
        if not self.alive:
            return 0

        dx = player_pos[0] - self.x
        dy = player_pos[1] - self.y
        distance_to_player = math.sqrt(dx * dx + dy * dy)

        # Если игрок близко - преследуем или атакуем
        if distance_to_player < 400:
            if distance_to_player > self.attack_range:
                # Преследование
                angle_to_player = math.atan2(dy, dx)
                new_x = self.x + self.speed * math.cos(angle_to_player)
                new_y = self.y + self.speed * math.sin(angle_to_player)

                # Проверка коллизии
                from ray_casting import mapping
                if mapping(new_x, new_y) not in world_map:
                    self.x = new_x
                    self.y = new_y
            else:
                # Атака
                if self.attack_cooldown <= 0:
                    self.attack_cooldown = 60
                    return self.attack_damage

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        return 0

    def take_damage(self, damage):
        """Получение урона"""
        self.health -= damage
        if self.health <= 0:
            self.alive = False
            return True  # Убит
        return False


class Slime(Sprite):
    """Слизень, который делится на меньших при смерти"""

    def __init__(self, x, y, textures_dict, size='large', scale_factor=None):
        # Размеры и характеристики в зависимости от размера
        self.size = size

        if size == 'large':
            self.health_max = 100
            self.speed = 1.0
            self.attack_damage = 15
            self.can_split = True
            scale = scale_factor or 0.8
        elif size == 'medium':
            self.health_max = 50
            self.speed = 1.5
            self.attack_damage = 10
            self.can_split = True
            scale = scale_factor or 0.5
        elif size == 'small':
            self.health_max = 25
            self.speed = 2.0
            self.attack_damage = 5
            self.can_split = False  # Маленькие не делятся
            scale = scale_factor or 0.3
        else:
            self.health_max = 100
            self.speed = 1.0
            self.attack_damage = 10
            self.can_split = False
            scale = scale_factor or 0.6

        super().__init__(x, y, textures_dict, scale)

        self.health = self.health_max
        self.attack_range = 80
        self.attack_cooldown = 0

    def get_split_size(self):
        """Возвращает размер слизней после деления"""
        if self.size == 'large':
            return 'medium'
        elif self.size == 'medium':
            return 'small'
        else:
            return None  # Маленькие не делятся

    def update(self, player_pos, world_map):
        """Обновление AI слизня"""
        if not self.alive:
            return 0

        dx = player_pos[0] - self.x
        dy = player_pos[1] - self.y
        distance_to_player = math.sqrt(dx * dx + dy * dy)

        # Преследование или атака
        if distance_to_player < 400:
            if distance_to_player > self.attack_range:
                # Преследование
                angle_to_player = math.atan2(dy, dx)
                new_x = self.x + self.speed * math.cos(angle_to_player)
                new_y = self.y + self.speed * math.sin(angle_to_player)

                from ray_casting import mapping
                if mapping(new_x, new_y) not in world_map:
                    self.x = new_x
                    self.y = new_y
            else:
                # Атака
                if self.attack_cooldown <= 0:
                    self.attack_cooldown = 60
                    return self.attack_damage

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        return 0

    def take_damage(self, damage):
        """Получение урона"""
        self.health -= damage
        if self.health <= 0:
            self.alive = False
            return True  # Убит
        return False

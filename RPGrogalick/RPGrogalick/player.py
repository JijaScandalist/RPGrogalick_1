# player.py
import sys
from settings import *
import pygame
import math
from equipment import Fireball
from map import world_map, floor_map
from ray_casting import mapping


class Player:
    def __init__(self):
        self.x, self.y = player_position
        self.angle = player_angle
        self.pitch = 0
        self.delta = 0
        self.fireballs = []
        self.height = player_height
        self.health = 100
        self.damage_timer = 0
        self.damage_interval = 60
        self.lava_damage = 5
        self.is_attacking = False
        self.attack_cooldown = 0
        self.is_dead = False
        self.on_staircase = False  # Флаг нахождения на лестнице

    @property
    def position(self):
        """Возвращает позицию игрока"""
        return (self.x, self.y)

    def movement(self):
        # Если мертв - не двигаемся
        if self.is_dead:
            return

        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        keys = pygame.key.get_pressed()

        # Ускорение при Ctrl
        speed = player_speed
        if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
            speed *= 3

        # Коллизия со стенами
        if keys[pygame.K_w]:
            nx = self.x + speed * cos_a
            ny = self.y + speed * sin_a
            if mapping(nx, ny) not in world_map:
                self.x = nx
                self.y = ny
        if keys[pygame.K_s]:
            nx = self.x - speed * cos_a
            ny = self.y - speed * sin_a
            if mapping(nx, ny) not in world_map:
                self.x = nx
                self.y = ny
        if keys[pygame.K_a]:
            nx = self.x + speed * sin_a
            ny = self.y - speed * cos_a
            if mapping(nx, ny) not in world_map:
                self.x = nx
                self.y = ny
        if keys[pygame.K_d]:
            nx = self.x - speed * sin_a
            ny = self.y + speed * cos_a
            if mapping(nx, ny) not in world_map:
                self.x = nx
                self.y = ny

        self.mouse_control()

        if keys[pygame.K_SPACE]:
            self.shoot()
        if keys[pygame.K_ESCAPE]:
            sys.exit()

        # Проверка нахождения на лестнице
        floor_tile_pos = mapping(self.x, self.y)
        self.on_staircase = floor_map.get(floor_tile_pos) == 'staircase'

        # Урон от лавы
        floor_tile_pos = mapping(self.x, self.y)
        floor_type = floor_map.get(floor_tile_pos, None)
        if floor_type in ['floor4', 'floor5']:
            self.damage_timer += 1
            if self.damage_timer >= self.damage_interval:
                self.take_damage(self.lava_damage)
                self.damage_timer = 0

    def take_damage(self, damage):
        """Получение урона с проверкой смерти"""
        self.health -= damage
        print(f"Получен урон {damage}! Здоровье: {self.health}")
        if self.health <= 0:
            self.health = 0
            self.is_dead = True
            print("GAME OVER! Игрок погиб!")

    def mouse_control(self):
        if pygame.mouse.get_focused():
            mouse_pos = pygame.mouse.get_pos()
            # Горизонтальное вращение
            difference_x = mouse_pos[0] - half_width
            self.angle += difference_x * 0.004

            # Вертикальное вращение
            difference_y = mouse_pos[1] - half_height
            self.pitch -= difference_y * 0.004

            # Ограничиваем вертикальный угол
            self.pitch = max(-1.5, min(1.5, self.pitch))

            # Возвращаем мышь в центр
            pygame.mouse.set_pos(half_width, half_height)

    def shoot(self):
        offset_x = math.cos(self.angle) * 20
        offset_y = math.sin(self.angle) * 20
        fireball = Fireball(self.x + offset_x, self.y + offset_y, self.angle)
        self.fireballs.append(fireball)

    def update_fireballs(self, enemies):
        for fireball in self.fireballs[:]:
            fireball.update(world_map, enemies)
            if not fireball.alive:
                self.fireballs.remove(fireball)

    def attack(self, enemies):
        """Атака мечом"""
        if self.is_dead or self.attack_cooldown > 0:
            return

        self.is_attacking = True
        self.attack_cooldown = 15  # Сокращаем кулдаун для более быстрых атак

        # Используем настройки из settings
        attack_range = player_attack_range
        attack_damage = 50

        hit_count = 0
        for enemy in enemies:
            if not enemy.alive:
                continue

            dx = enemy.x - self.x
            dy = enemy.y - self.y
            distance = math.sqrt(dx * dx + dy * dy)

            # Проверяем расстояние
            if distance < attack_range:
                # Проверяем угол
                enemy_angle = math.atan2(dy, dx)
                angle_diff = enemy_angle - self.angle

                # Нормализуем
                while angle_diff > math.pi:
                    angle_diff -= 2 * math.pi
                while angle_diff < -math.pi:
                    angle_diff += 2 * math.pi

                if abs(angle_diff) < attack_angle:  # Используем из settings
                    killed = enemy.take_damage(attack_damage)
                    hit_count += 1
                    print(f"Удар! Расстояние: {int(distance)}, Здоровье врага: {enemy.health}")
                    if killed:
                        print(f"Враг убит!")

        if hit_count == 0:
            print("Атака в промах!")

    # Добавьте этот метод в класс Player для полного сброса состояния
    def reset(self):
        """Сбрасывает состояние игрока (при перезапуске уровня)"""
        self.x, self.y = player_position
        self.angle = player_angle
        self.pitch = 0
        self.fireballs = []
        self.health = 100
        self.damage_timer = 0
        self.is_attacking = False
        self.attack_cooldown = 0
        self.is_dead = False
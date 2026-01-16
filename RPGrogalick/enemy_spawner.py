import pygame
from sprites import Enemy, Slime
from settings import *


class EnemySpawner:
    def __init__(self, textures_dict):
        self.textures = textures_dict
        self.enemies = []
        self.spawn_queue = []  # Очередь для отложенного спавна (при делении слизней)

    def spawn_slime(self, x, y, size='large'):
        """Создаёт слизня определённого размера"""
        slime_textures = {
            'front': self.textures[f'slime_{size}_front'],
            'back': self.textures[f'slime_{size}_back'],
            'left': self.textures[f'slime_{size}_left'],
            'right': self.textures[f'slime_{size}_right'],
            'front_left': self.textures[f'slime_{size}_left'],
            'front_right': self.textures[f'slime_{size}_right'],
            'back_left': self.textures[f'slime_{size}_left'],
            'back_right': self.textures[f'slime_{size}_right'],
        }

        slime = Slime(x, y, slime_textures, size)
        self.enemies.append(slime)
        return slime

    def spawn_enemy(self, x, y, enemy_type='slime', size='large'):
        """Универсальный метод для создания врагов"""
        if enemy_type == 'slime':
            return self.spawn_slime(x, y, size)
        # Можно добавить других врагов
        # elif enemy_type == 'skeleton':
        #     return self.spawn_skeleton(x, y)

    def update(self, player_pos, world_map):
        """Обновляет всех врагов и обрабатывает деление слизней"""
        total_damage = 0

        for enemy in self.enemies[:]:
            if not enemy.alive:
                # Если слизень погиб и может делиться
                if isinstance(enemy, Slime) and enemy.can_split:
                    # Добавляем в очередь спавна два маленьких слизня
                    new_size = enemy.get_split_size()
                    if new_size:
                        offset = 30
                        self.spawn_queue.append({
                            'x': enemy.x - offset,
                            'y': enemy.y - offset,
                            'size': new_size
                        })
                        self.spawn_queue.append({
                            'x': enemy.x + offset,
                            'y': enemy.y + offset,
                            'size': new_size
                        })

                self.enemies.remove(enemy)
                continue

            damage = enemy.update(player_pos, world_map)
            total_damage += damage

        # Спавним отложенных врагов (маленьких слизней)
        for spawn_data in self.spawn_queue:
            self.spawn_slime(spawn_data['x'], spawn_data['y'], spawn_data['size'])
        self.spawn_queue.clear()

        return total_damage

    def get_enemies(self):
        """Возвращает список всех живых врагов"""
        return [e for e in self.enemies if e.alive]

    def clear_all(self):
        """Удаляет всех врагов"""
        self.enemies.clear()
        self.spawn_queue.clear()


# =============== КОНФИГУРАЦИЯ СПАВНА ===============
def create_level_enemies(spawner):
    """Создаёт врагов для уровня"""

    # УРОВЕНЬ 1: Базовые слизни
    spawner.spawn_slime(400, 400, 'large')
    spawner.spawn_slime(700, 300, 'large')
    spawner.spawn_slime(300, 600, 'medium')

    # Можно добавить конфигурацию для разных уровней:
    # if level == 1:
    #     spawner.spawn_slime(400, 400, 'large')
    # elif level == 2:
    #     spawner.spawn_slime(400, 400, 'large')
    #     spawner.spawn_slime(600, 600, 'large')

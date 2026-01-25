import pygame
from sprites import Enemy, Slime
from settings import *
import random
from map import world_map, floor_map


class EnemySpawner:
    def __init__(self, textures_dict):
        self.textures = textures_dict
        self.enemies = []
        self.spawn_queue = []  # Очередь для отложенного спавна (при делении слизней)
        self.enemy_count_multiplier = 1.0  # Множитель для количества врагов

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

    def count_alive_enemies(self):
        """Возвращает количество живых врагов"""
        return len([e for e in self.enemies if e.alive])

    def clear_all(self):
        """Удаляет всех врагов"""
        self.enemies.clear()
        self.spawn_queue.clear()

    def set_difficulty(self, level):
        """Устанавливает сложность в зависимости от уровня"""
        self.enemy_count_multiplier = 1.0 + (level - 1) * 0.5


# КОНФИГ СПАВНА
def create_level_enemies(spawner, level=1):
    """Создаёт врагов для уровня с учётом множителя"""
    # Импортируем актуальные карты для работы с координатами
    from map import world_map, floor_map

    # Устанавливаем множитель в зависимости от уровня
    spawner.set_difficulty(level)

    # Для первого уровня используем статичный спавн
    if level == 1:
        spawner.spawn_slime(400, 400, 'large')
        spawner.spawn_slime(700, 300, 'large')
        spawner.spawn_slime(300, 600, 'medium')
        return



    # Находим зоны для спавна: только свободные места на полу, не в лаве и без стен
    spawn_zones = []

    # Перебираем все позиции пола
    for pos, tile_type in floor_map.items():
        x, y = pos

        # Пропускаем нежелательные зоны:
        # - лава
        if tile_type in ['floor4', 'floor5', 'floor3']:
            continue

        # - слишком близко к границам карты
        if x < 150 or y < 150 or x > width - 150 or y > height - 150:
            continue

        # - места, где есть стены
        if (x, y) in world_map:
            continue

        # - места слишком близко к центру (где спавнится игрок)
        if 300 < x < 900 and 300 < y < 500:
            continue

        spawn_zones.append((x, y))

    # Если мало зон для спавна, используем более мягкие критерии
    if len(spawn_zones) < 10:
        spawn_zones = []
        for pos, tile_type in floor_map.items():
            x, y = pos
            if tile_type not in ['floor4', 'floor5'] and (x, y) not in world_map:
                if 100 < x < width - 100 and 100 < y < height - 100:
                    spawn_zones.append((x, y))

    # Перемешиваем зоны для случайности
    random.shuffle(spawn_zones)

    # Количество врагов зависит от уровня
    num_large = int(2 * spawner.enemy_count_multiplier)
    num_medium = int(3 * spawner.enemy_count_multiplier)
    num_small = int(5 * spawner.enemy_count_multiplier)

    print(f"Спавн врагов на уровне {level}: {num_large} больших, {num_medium} средних, {num_small} маленьких")
    print(f"Доступно зон для спавна: {len(spawn_zones)}")

    # Спавним врагов только в доступных зонах
    spawned_count = 0

    # Большие слизни
    for i in range(min(num_large, len(spawn_zones))):
        x, y = spawn_zones[i]
        spawner.spawn_slime(x, y, 'large')
        spawned_count += 1

    # Средние слизни
    for i in range(min(num_medium, len(spawn_zones) - num_large)):
        if num_large + i < len(spawn_zones):
            x, y = spawn_zones[num_large + i]
            spawner.spawn_slime(x, y, 'medium')
            spawned_count += 1

    # Маленькие слизни
    for i in range(min(num_small, len(spawn_zones) - num_large - num_medium)):
        if num_large + num_medium + i < len(spawn_zones):
            x, y = spawn_zones[num_large + num_medium + i]
            spawner.spawn_slime(x, y, 'small')
            spawned_count += 1

    print(f"Всего заспавнено врагов: {spawned_count}")

    # Если не удалось заспавнить достаточно врагов, добавим их в безопасные зоны
    if spawned_count < num_large + num_medium + num_small:
        print("Предупреждение: недостаточно безопасных зон для спавна всех врагов")
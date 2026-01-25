import random
from settings import *


class LevelManager:
    def __init__(self):
        self.current_level = 0  # 0 = tutorial
        self.ladder_position = None
        self.all_enemies_defeated = False

    def get_tutorial_map(self):
        """Возвращает обучающий уровень (тот что у вас есть)"""
        text_map = [
            '3333333333333333',
            '3...3..1...1...3',
            '3..1.....2..1..3',
            '3.......22.....3',
            '3..3....2..3...3',
            '3..3...R.1.....3',
            '3....R.........3',
            '3333333333333333'
        ]

        floor_map = [
            '33333333333333333333333333333333',
            '33333333333333333333333333333333',
            '33333333333333333333333333333333',
            '33333333333333333333333333333333',
            '33333333333333333333333333333333',
            '33333333544535333333333333333333',
            '33333333544453333333333333333333',
            '33333333333333333333333333333333',
        ]

        # Позиция лестницы (в клетках)
        ladder_pos = (2, 2)

        return text_map, floor_map, ladder_pos

    def generate_procedural_level(self, level_number):
        """Процедурная генерация уровня"""
        # Размер карты увеличивается с уровнем
        size = min(16 + level_number * 2, 30)

        # Инициализация пустой карты
        text_map = []
        floor_map = []

        for y in range(size):
            row = []
            floor_row = []
            for x in range(size):
                # Границы - всегда стены
                if x == 0 or x == size - 1 or y == 0 or y == size - 1:
                    row.append('3')
                    floor_row.append('3')
                else:
                    # Случайные стены (чем выше уровень, тем больше стен)
                    wall_chance = 0.15 + (level_number * 0.02)
                    if random.random() < wall_chance:
                        wall_type = random.choice(['1', '2', '3', 'R'])
                        row.append(wall_type)
                        floor_row.append('3')
                    else:
                        row.append('.')
                        # Случайный пол
                        floor_type = random.choice(['1', '2', '3', '3', '3'])  # Больше обычного пола
                        floor_row.append(floor_type)

            text_map.append(''.join(row))
            floor_map.append(''.join(floor_row))

        # Убедимся что есть проходимый путь (упрощенная версия)
        self._ensure_path(text_map, size)

        # Добавляем опасные зоны (лаву) на высоких уровнях
        if level_number > 2:
            self._add_lava_zones(floor_map, size, level_number)

        # Позиция лестницы - случайная, но не у стены
        ladder_x = random.randint(2, size - 3)
        ladder_y = random.randint(2, size - 3)

        # Убедимся что там нет стены
        while text_map[ladder_y][ladder_x] != '.':
            ladder_x = random.randint(2, size - 3)
            ladder_y = random.randint(2, size - 3)

        ladder_pos = (ladder_x, ladder_y)

        return text_map, floor_map, ladder_pos

    def _ensure_path(self, text_map, size):
        """Убирает изолированные стены для проходимости"""
        # Простая очистка центральной области
        center_size = size // 3
        start_x = size // 2 - center_size // 2
        start_y = size // 2 - center_size // 2

        for y in range(start_y, start_y + center_size):
            for x in range(start_x, start_x + center_size):
                if 0 < y < len(text_map) and 0 < x < len(text_map[0]):
                    row = list(text_map[y])
                    if random.random() > 0.3:  # 70% шанс убрать стену
                        row[x] = '.'
                    text_map[y] = ''.join(row)

    def _add_lava_zones(self, floor_map, size, level_number):
        """Добавляет зоны лавы на карту"""
        num_lava_zones = min(level_number - 2, 5)  # Максимум 5 зон

        for _ in range(num_lava_zones):
            # Случайная позиция для зоны лавы
            lava_x = random.randint(3, size - 4)
            lava_y = random.randint(3, size - 4)
            lava_size = random.randint(2, 4)

            # Создаем зону лавы
            for dy in range(lava_size):
                for dx in range(lava_size):
                    y = lava_y + dy
                    x = lava_x + dx
                    if 0 < y < len(floor_map) and 0 < x < len(floor_map[0]):
                        row = list(floor_map[y])
                        lava_type = random.choice(['4', '5'])  # floor4 или floor5
                        row[x] = lava_type
                        floor_map[y] = ''.join(row)

    def get_level_data(self, level_number):
        """Возвращает данные уровня"""
        if level_number == 0:
            return self.get_tutorial_map()
        else:
            return self.generate_procedural_level(level_number)

    def check_ladder_collision(self, player_pos):
        """Проверяет, стоит ли игрок на лестнице"""
        if self.ladder_position is None:
            return False

        ladder_x, ladder_y = self.ladder_position
        ladder_world_x = ladder_x * tile + tile // 2
        ladder_world_y = ladder_y * tile + tile // 2

        px, py = player_pos
        distance = ((px - ladder_world_x) ** 2 + (py - ladder_world_y) ** 2) ** 0.5

        return distance < 50  # Радиус активации лестницы

    def update_enemies_status(self, enemies):
        """Обновляет статус врагов"""
        alive_enemies = [e for e in enemies if e.alive]
        self.all_enemies_defeated = len(alive_enemies) == 0
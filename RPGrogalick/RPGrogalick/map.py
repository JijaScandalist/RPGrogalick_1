from settings import *
import random

# КАРТА СТЕН
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

# КАРТА ПОЛА
floor_text_map = [
    '3333333333333333',
    '3333333333333333',
    '3333333333333333',
    '3333333333333333',
    '3333333333333333',
    '3333333354453533',
    '3S33333354445333',  # Лестница
    '3333333333333333'
]

# Словари для хранения карт
world_map = {}
floor_map = {}
ceiling_map = {}
mini_map = set()

# Обработка карты СТЕН
for j, row in enumerate(text_map):
    for i, char in enumerate(row):
        if char != '.':
            mini_map.add((i * map_tile, j * map_tile))
            if char == '1':
                world_map[(i * tile, j * tile)] = '1'
            elif char == '2':
                world_map[(i * tile, j * tile)] = '2'
            elif char == '3':
                world_map[(i * tile, j * tile)] = '3'
            elif char == 'R':
                world_map[(i * tile, j * tile)] = 'R'

# Обработка карты ПОЛА
for j, row in enumerate(floor_text_map):
    for i, char in enumerate(row):
        if char != '0' and char != '.':  # 0 или . = пустота (нет пола)
            pos = (i * tile, j * tile)
            if char == '1':
                floor_map[pos] = 'floor1'
            elif char == '2':
                floor_map[pos] = 'floor2'
            elif char == '3':
                floor_map[pos] = 'floor3'
            elif char == '4':
                floor_map[pos] = 'floor4'
            elif char == '5':
                floor_map[pos] = 'floor5'
            elif char == 'S':  # Обработка лестницы
                floor_map[pos] = 'staircase'


def mapping(a, b):
    return (a // tile) * tile, (b // tile) * tile


def generate_level(level_num):
    """Генерирует карту для указанного уровня"""
    global text_map, floor_text_map, world_map, floor_map, mini_map

    # Очистка текущих карт
    world_map.clear()
    floor_map.clear()
    mini_map.clear()

    if level_num == 1:
        # Для первого уровня используем статичную карту
        print("Загружаем статичную карту для уровня 1")

        # Сбрасываем карты к исходным значениям
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

        floor_text_map = [
            '3333333333333333',
            '3333333333333333',
            '3333333333333333',
            '3333333333333333',
            '3333333333333333',
            '3333333354453533',
            '3S33333354445333',  # Лестница
            '3333333333333333'
        ]

        # Обработка карты СТЕН
        for j, row in enumerate(text_map):
            for i, char in enumerate(row):
                if char != '.':
                    mini_map.add((i * map_tile, j * map_tile))
                    if char == '1':
                        world_map[(i * tile, j * tile)] = '1'
                    elif char == '2':
                        world_map[(i * tile, j * tile)] = '2'
                    elif char == '3':
                        world_map[(i * tile, j * tile)] = '3'
                    elif char == 'R':
                        world_map[(i * tile, j * tile)] = 'R'

        # Обработка карты ПОЛА
        for j, row in enumerate(floor_text_map):
            for i, char in enumerate(row):
                if char != '0' and char != '.':  # 0 или . = пустота (нет пола)
                    pos = (i * tile, j * tile)
                    if char == '1':
                        floor_map[pos] = 'floor1'
                    elif char == '2':
                        floor_map[pos] = 'floor2'
                    elif char == '3':
                        floor_map[pos] = 'floor3'
                    elif char == '4':
                        floor_map[pos] = 'floor4'
                    elif char == '5':
                        floor_map[pos] = 'floor5'
                    elif char == 'S':  # Лестница
                        floor_map[pos] = 'staircase'

        print("Статичная карта уровня 1 загружена")
        return [(1, 1, 5, 4), (1, 6, 2, 1)]  # Пример комнат для уровня 1

    # Для уровней 2+ используем процедурную генерацию
    # Размеры карты в зависимости от уровня
    base_width = 16
    base_height = 8
    map_width = base_width + (level_num - 1) * 4
    map_height = base_height + (level_num - 1) * 2

    # минимальный размер карты
    map_width = max(map_width, 16)
    map_height = max(map_height, 10)

    print(f"Генерация уровня {level_num} с размерами {map_width}x{map_height}")

    # Инициализация карт
    # ВСЕ ячейки по умолчанию - стены ('3')
    text_map = [['3' for _ in range(map_width)] for _ in range(map_height)]
    floor_text_map = [['1' for _ in range(map_width)] for _ in range(map_height)]  # Весь пол покрыт плиткой

    # Создание комнат
    num_rooms = 2 + level_num  # Количество комнат зависит от уровня
    rooms = []

    # Добавляем начальную комнату для игрока
    start_room_width = min(5, max(3, map_width // 4))
    start_room_height = min(4, max(3, map_height // 4))
    start_room_x = 1
    start_room_y = 1
    rooms.append((start_room_x, start_room_y, start_room_width, start_room_height))

    # Заполняем начальную комнату (убираем стены внутри)
    for j in range(start_room_y, start_room_y + start_room_height):
        for i in range(start_room_x, start_room_x + start_room_width):
            if 0 <= j < map_height and 0 <= i < map_width:
                text_map[j][i] = '.'  # Пустое пространство вместо стены

    # Остальные комнаты
    for _ in range(num_rooms - 1):
        max_room_width = min(7, max(3, map_width // 4))
        max_room_height = min(5, max(3, map_height // 4))

        room_width = random.randint(3, max_room_width)
        room_height = random.randint(3, max_room_height)

        # Находим подходящую позицию для комнаты
        max_attempts = 50
        room_created = False

        for attempt in range(max_attempts):
            x = random.randint(2, max(2, map_width - room_width - 2))
            y = random.randint(2, max(2, map_height - room_height - 2))

            # Проверяем, не пересекается ли комната со стенами или другими комнатами
            valid_position = True
            for j in range(max(0, y - 1), min(map_height, y + room_height + 1)):
                for i in range(max(0, x - 1), min(map_width, x + room_width + 1)):
                    if text_map[j][i] != '3' and text_map[j][i] != '.':  # Проверяем только стены и пустоту
                        valid_position = False
                        break
                if not valid_position:
                    break

            if valid_position:
                # Создаем комнату
                for j in range(y, min(map_height, y + room_height)):
                    for i in range(x, min(map_width, x + room_width)):
                        if 0 <= j < map_height and 0 <= i < map_width:
                            text_map[j][i] = '.'  # Убираем стены внутри комнаты

                rooms.append((x, y, room_width, room_height))
                room_created = True
                break

    # Если не удалось создать достаточно комнат, создаем хотя бы минимум
    if len(rooms) < 2:
        # Добавляем комнату для лестницы
        end_room_width = min(4, max(3, map_width // 5))
        end_room_height = min(4, max(3, map_height // 5))
        end_room_x = max(1, map_width - end_room_width - 2)
        end_room_y = max(1, map_height - end_room_height - 2)

        for j in range(end_room_y, min(map_height, end_room_y + end_room_height)):
            for i in range(end_room_x, min(map_width, end_room_x + end_room_width)):
                if 0 <= j < map_height and 0 <= i < map_width:
                    text_map[j][i] = '.'
        rooms.append((end_room_x, end_room_y, end_room_width, end_room_height))

    # Соединение комнат коридорами
    for i in range(len(rooms) - 1):
        x1, y1, w1, h1 = rooms[i]
        x2, y2, w2, h2 = rooms[i + 1]

        # Центры комнат
        cx1, cy1 = x1 + w1 // 2, y1 + h1 // 2
        cx2, cy2 = x2 + w2 // 2, y2 + h2 // 2

        # Горизонтальный коридор
        start_x = min(cx1, cx2)
        end_x = max(cx1, cx2)
        for x in range(start_x, end_x + 1):
            if 0 <= cy1 < map_height and 0 <= x < map_width:
                text_map[cy1][x] = '.'  # Пробиваем коридор через стены

        # Вертикальный коридор
        start_y = min(cy1, cy2)
        end_y = max(cy1, cy2)
        for y in range(start_y, end_y + 1):
            if 0 <= cx2 < map_width and 0 <= y < map_height:
                text_map[y][cx2] = '.'  # Пробиваем коридор через стены

    # Добавление дополнительных стен внутри комнат для сложности
    if level_num > 1 and rooms:
        max_walls = min(8, (map_width + map_height) // 5)
        for _ in range(max_walls):
            room = random.choice(rooms)
            x, y, w, h = room

            # Добавляем стены только в достаточно больших комнатах
            if w < 5 or h < 5:
                continue

            # Создаем внутреннюю стену
            wall_x = random.randint(x + 1, x + w - 2)
            wall_y = random.randint(y + 1, y + h - 2)
            wall_length = random.randint(1, min(3, w - 3))

            # Вероятность вертикальной или горизонтальной стены
            if random.random() > 0.5:
                # Горизонтальная стена
                for i in range(wall_x, min(wall_x + wall_length, x + w - 1)):
                    if 0 <= wall_y < map_height and 0 <= i < map_width:
                        text_map[wall_y][i] = '3'  # Добавляем стену
            else:
                # Вертикальная стена
                for j in range(wall_y, min(wall_y + wall_length, y + h - 1)):
                    if 0 <= j < map_height and 0 <= wall_x < map_width:
                        text_map[j][wall_x] = '3'  # Добавляем стену

    # Добавление лавы на более высоких уровнях
    if level_num >= 2 and rooms:
        num_lava_zones = min(5, level_num)
        for _ in range(num_lava_zones):
            if len(rooms) > 1:
                room = random.choice(rooms[1:])  # Исключаем начальную комнату
                x, y, w, h = room

                if w >= 4 and h >= 4:  # Только в достаточно больших комнатах
                    lava_x = random.randint(x + 1, x + w - 2)
                    lava_y = random.randint(y + 1, y + h - 2)
                    lava_size = random.randint(1, min(2, w - 2, h - 2))

                    for j in range(lava_y, min(lava_y + lava_size, y + h, map_height)):
                        for i in range(lava_x, min(lava_x + lava_size, x + w, map_width)):
                            if 0 <= j < map_height and 0 <= i < map_width:
                                floor_text_map[j][i] = '4'  # Лава

    # Преобразование карт в строки для совместимости
    text_map = [''.join(row) for row in text_map]
    floor_text_map = [''.join(row) for row in floor_text_map]

    # Добавление лестницы в последней комнате
    if rooms:
        last_room = rooms[-1]
        stair_x = last_room[0] + last_room[2] // 2
        stair_y = last_room[1] + last_room[3] // 2

        stair_x = max(1, min(stair_x, map_width - 2))
        stair_y = max(1, min(stair_y, map_height - 2))

        if stair_y < len(floor_text_map) and stair_x < len(floor_text_map[stair_y]):
            # Создаем копию строки с лестницей
            row = list(floor_text_map[stair_y])
            if stair_x < len(row):
                row[stair_x] = 'S'  # Символ лестницы
            floor_text_map[stair_y] = ''.join(row)

    # Перезагрузка карт из обновленных массивов
    world_map.clear()
    floor_map.clear()
    mini_map.clear()

    # ОБРАБОТКА КАРТЫ СТЕН
    wall_count = 0
    for j, row in enumerate(text_map):
        for i, char in enumerate(row):
            if char != '.':  # Если не пустое пространство - это стена
                wall_count += 1
                mini_map.add((i * map_tile, j * map_tile))
                if char == '1':
                    world_map[(i * tile, j * tile)] = '1'
                elif char == '2':
                    world_map[(i * tile, j * tile)] = '2'
                elif char == '3':
                    world_map[(i * tile, j * tile)] = '3'
                elif char == 'R':
                    world_map[(i * tile, j * tile)] = 'R'

    print(f"Сгенерировано {wall_count} блоков стен")

    # ОБРАБОТКА КАРТЫ ПОЛА
    floor_count = 0
    for j, row in enumerate(floor_text_map):
        for i, char in enumerate(row):
            if char != '0' and char != '.':  # 0 или . = пустота (нет пола)
                floor_count += 1
                pos = (i * tile, j * tile)
                if char == '1':
                    floor_map[pos] = 'floor1'
                elif char == '2':
                    floor_map[pos] = 'floor2'
                elif char == '3':
                    floor_map[pos] = 'floor3'
                elif char == '4':
                    floor_map[pos] = 'floor4'
                elif char == '5':
                    floor_map[pos] = 'floor5'
                elif char == 'S':  # Лестница
                    floor_map[pos] = 'staircase'

    print(f"Сгенерировано {floor_count} блоков пола")
    print(f"Уровень {level_num} сгенерирован. Количество комнат: {len(rooms)}")
    return rooms
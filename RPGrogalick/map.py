# from settings import *
#
# text_map = [
#     '3333333333333333',
#     '3......1...1...3',
#     '3..1.....2..1..3',
#     '3.......22.....3',
#     '3..3....2..3...3',
#     '3..3...2.1.....3',
#     '3....3.........3',
#     '3333333333333333'
# ]
#
# world_map = {}
# mini_map = set()
# for j, row in enumerate(text_map):
#     for i, char in enumerate(row):
#         if char != '.':
#             mini_map.add((i * map_tile, j * map_tile))
#             if char == '1':
#                 world_map[(i * tile, j * tile)] = '1'
#             elif char == '2':
#                 world_map[(i * tile, j * tile)] = '2'
#             elif char == '3':
#                 world_map[(i * tile, j * tile)] = '3'
#map


from settings import *

# КАРТА СТЕН (как было)
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

# НОВОЕ: КАРТА ПОЛА (точно так же как text_map!)
# Здесь каждая цифра = текстура пола
# 0 = нет пола (пустота), 1 = floor1, 2 = floor2, и т.д.
floor_text_map = [
    '33333333333333333333333333333333',
    '33333333333333333333333333333333',
    '33333333333333333333333333333333',
    '33333333333333333333333333333333',
    '33333333333333333333333333333333',
    '33333333544535333333333333333333',
    '33333333544453333333333333333333',
    '33333333333333333333333333333333',
    '33333333333333333333333333333333',
    '33333333333333333333333333333333',
    '33333333333333333333333333333333',
    '33333333333333333333333333333333',
    '33333333333333333333333333333333',
    '33333333333333333333333333333333',

]

# НОВОЕ: КАРТА ПОТОЛКА (опционально)
ceiling_text_map = [
    '0000000000000000',
    '0000000000000000',
    '0000000000000000',
    '0000000000000000',
    '0000000000000000',
    '0000000000000000',
    '0000000000000000',
    '0000000000000000'
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


# НОВОЕ: Обработка карты ПОЛА
for j, row in enumerate(floor_text_map):
    for i, char in enumerate(row):
        if char != '0' and char != '.':  # 0 или . = пустота (нет пола)
            if char == '1':
                floor_map[(i * tile, j * tile)] = 'floor1'
            elif char == '2':
                floor_map[(i * tile, j * tile)] = 'floor2'
            elif char == '3':
                floor_map[(i * tile, j * tile)] = 'floor3'
            elif char == '4':
                floor_map[(i * tile, j * tile)] = 'floor4'
            elif char == '5':
                floor_map[(i * tile, j * tile)] = 'floor5'
            # Можно добавить больше текстур пола

# НОВОЕ: Обработка карты ПОТОЛКА
for j, row in enumerate(ceiling_text_map):
    for i, char in enumerate(row):
        if char != '0' and char != '.':
            if char == '1':
                ceiling_map[(i * tile, j * tile)] = 'ceiling1'
            elif char == '2':
                ceiling_map[(i * tile, j * tile)] = 'ceiling2'
            elif char == '3':
                ceiling_map[(i * tile, j * tile)] = 'ceiling3'

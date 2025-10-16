from settings import *

text_map = [
    '3333333333333333',
    '3......1...1...3',
    '3..1.....2..1..3',
    '3.......22.....3',
    '3..3....2..3...3',
    '3..3...2.1.....3',
    '3....3.........3',
    '3333333333333333'
]

world_map = {}
mini_map = set()
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
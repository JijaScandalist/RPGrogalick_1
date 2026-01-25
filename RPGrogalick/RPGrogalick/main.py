#main
import pygame
from settings import *
from player import Player
from map import world_map, floor_map, mapping, generate_level
from drawing import Drawing
from enemy_spawner import EnemySpawner, create_level_enemies
import math
pygame.init()
sc = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
player = Player()
drawing = Drawing(sc, None)
pygame.mouse.set_visible(False)

# Создаём систему спавна врагов
spawner = EnemySpawner(drawing.textures)
create_level_enemies(spawner, current_level)

# Флаги для управления уровнями
level_completed = False
staircase_active = False
level_transition = False
show_staircase_hint = False


def check_staircase_interaction():
    """Проверяет, может ли игрок взаимодействовать с лестницей"""
    global staircase_active, staircase_pos

    # Ищем позицию лестницы на карте
    staircase_pos = None
    for pos, texture in floor_map.items():
        if texture == 'staircase':
            staircase_pos = pos
            break

    if staircase_pos is None:
        return False

    # Проверяем, все ли враги побеждены
    if spawner.count_alive_enemies() == 0:
        staircase_active = True
    else:
        staircase_active = False

    # Проверяем расстояние до лестницы
    dx = staircase_pos[0] + tile // 2 - player.x
    dy = staircase_pos[1] + tile // 2 - player.y
    distance = math.sqrt(dx * dx + dy * dy)

    return staircase_active and distance < staircase_radius


def next_level():
    """Переход на следующий уровень"""
    global current_level, level_completed, level_transition

    current_level += 1
    level_completed = False
    level_transition = True

    # Генерация нового уровня
    generate_level(current_level)

    # Обновление позиции игрока (в начало уровня)
    player.x, player.y = 150, 150
    player.health = 100
    player.is_dead = False

    # Очистка и создание новых врагов
    spawner.clear_all()

    # Импортируем world_map после генерации уровня
    from map import world_map

    create_level_enemies(spawner, current_level)

    level_transition = False


# Ищем начальную позицию лестницы
staircase_pos = None
for pos, texture in floor_map.items():
    if texture == 'staircase':
        staircase_pos = pos
        break

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        # Атака по клику мыши
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not player.is_dead:  # ЛКМ
                player.attack(spawner.get_enemies())

        # Взаимодействие с лестницей
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e and check_staircase_interaction() and current_level < max_levels:
                next_level()

    # Если уровень завершен и лестница активна
    if spawner.count_alive_enemies() == 0 and not level_completed:
        level_completed = True

    # Обновляем кулдаун даже если игрок мертв
    if player.attack_cooldown > 0:
        player.attack_cooldown -= 1

    # Сброс анимации атаки только когда кулдаун закончился
    if player.attack_cooldown <= 0:
        player.is_attacking = False

    if not player.is_dead:
        player.movement()
        # Обновляем врагов 
        damage = spawner.update(player.position, world_map)
        if damage > 0:
            player.take_damage(damage)

    # Экран смерти или перехода на новый уровень
    if player.is_dead or level_transition:
        font = pygame.font.SysFont('Arial', 72, bold=True)
        if player.is_dead:
            message = font.render('GAME OVER', True, (255, 0, 0))
            sub_message = pygame.font.SysFont('Arial', 36).render('Press R to restart or ESC to quit', True,
                                                                  (255, 255, 255))
        else:
            message = font.render(f'LEVEL {current_level} COMPLETE!', True, (0, 255, 0))
            sub_message = pygame.font.SysFont('Arial', 36).render('Preparing next level...', True, (255, 255, 255))

        sc.fill(black)
        sc.blit(message, (width // 2 - message.get_width() // 2, height // 2 - 50))
        sc.blit(sub_message, (width // 2 - sub_message.get_width() // 2, height // 2 + 50))
        pygame.display.flip()

        if player.is_dead:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                # Перезапуск уровня
                player = Player()
                spawner.clear_all()
                create_level_enemies(spawner, current_level)
            if keys[pygame.K_ESCAPE]:
                exit()

        clock.tick(10)
        continue

    if not player.is_dead:
        player.movement()

    sc.fill(black)

    # Отрисовка
    drawing.background(player.angle)
    drawing.world(player)
    drawing.sprites(player, spawner.get_enemies())
    drawing.weapon(player.is_attacking)
    drawing.crosshair()
    drawing.fps(clock)
    drawing.health(player.health)
    # Счетчик врагов
    drawing.enemy_counter(len(spawner.get_enemies()))

    # Проверка взаимодействия с лестницей
    show_staircase_hint = check_staircase_interaction()
    if staircase_pos and show_staircase_hint:
        dx = staircase_pos[0] + tile // 2 - player.x
        dy = staircase_pos[1] + tile // 2 - player.y
        distance = math.sqrt(dx * dx + dy * dy)
        if distance < 200:  # Показывать подсказку, когда игрок рядом
            drawing.staircase_hint(spawner.count_alive_enemies() == 0)

    pygame.display.flip()
    clock.tick(fps)
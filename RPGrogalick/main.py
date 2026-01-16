import pygame
from settings import *
from player import Player
from map import world_map
from drawing import Drawing
from enemy_spawner import EnemySpawner, create_level_enemies

pygame.init()
sc = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
player = Player()
drawing = Drawing(sc, None)
pygame.mouse.set_visible(False)

# Создаём систему спавна врагов
spawner = EnemySpawner(drawing.textures)
create_level_enemies(spawner)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        # Атака по клику мыши
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # ЛКМ
                player.attack(spawner.get_enemies())

    player.movement()

    # Обновляем врагов (включая деление слизней)
    damage = spawner.update(player.position, world_map)
    if damage > 0:
        player.take_damage(damage)

    # Сброс анимации атаки
    if player.attack_cooldown == 0:
        player.is_attacking = False

    sc.fill(black)

    # Отрисовка
    drawing.background(player.angle)
    drawing.world(player)
    drawing.sprites(player, spawner.get_enemies())
    drawing.weapon(player.is_attacking)
    drawing.crosshair()
    drawing.fps(clock)
    drawing.health(player.health)

    # Экран смерти
    if player.is_dead:
        font = pygame.font.SysFont('Arial', 72, bold=True)
        game_over_text = font.render('GAME OVER', True, (255, 0, 0))
        restart_text = pygame.font.SysFont('Arial', 36).render('Press R to restart or ESC to quit', True,
                                                               (255, 255, 255))

        sc.blit(game_over_text, (width // 2 - 200, height // 2 - 50))
        sc.blit(restart_text, (width // 2 - 250, height // 2 + 50))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            # Перезапуск
            player = Player()
            spawner.clear_all()
            create_level_enemies(spawner)
        if keys[pygame.K_ESCAPE]:
            exit()

    pygame.display.flip()
    clock.tick(fps)

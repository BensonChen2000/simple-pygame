import pygame
import sys
import player
import menu
import background
import const
from pygame.locals import *
import shop
import enemy
import in_game_menu
clock = pygame.time.Clock()

background.pygame.init()  # initiates pygame

background.pygame.display.set_caption('Pygame Platformer', 'r')
maps = ['map.txt', 'map2.txt']

screen = background.pygame.display.set_mode(const.WINDOW_SIZE)  # initiate the window
player_one = player.players(const.PLAYER1_IMAGE, const.POS_X, const.POS_Y, const.X_SIZE, const.Y_SIZE)

level = 0

portal_group = pygame.sprite.Group()
portal_one = background.portal(288, 80)
portal_group.add(portal_one)

portal_collide = False

enemy_one = enemy.enemy(const.ENEMY_IMAGE, 100, 90, const.TILE_SIZE, const.TILE_SIZE)
enemy_two = enemy.enemy(const.ENEMY_IMAGE, 150, 40, const.TILE_SIZE, const.TILE_SIZE)

enemy_group = pygame.sprite.Group()
enemy_group.add(enemy_one)
enemy_group.add(enemy_two)



while True:  # game loop

    screen.fill(const.BLUE)
    display, tile_rects = background.map(maps[level])
    player_rect = player_one.player_move(tile_rects)
    enemy_rect_one = enemy_one.move(tile_rects)
    enemy_rect_two = enemy_two.move(tile_rects)
    enemy_one.update(enemy_rect_one)
    enemy_two.update(enemy_rect_two)
    #in_game_menu.main()
    portal_collide = pygame.sprite.spritecollide(player_one, portal_group, False)
    if len(portal_collide) > 0:

        if level < const.MAX_LEVEL:
            level += 1
            player_one.life += 1
            player_rect.x = const.POS_X
            player_rect.y = const.POS_Y
            upgrades = shop.Shop()
            player_one.moving_right = True
            player_one.moving_right = False

            if upgrades['Speed Boost']:
                const.HORI_VEL += 1
            elif upgrades['Jump Boost']:
                const.JUMP_HEIGHT += 1
            elif upgrades['Extra Life']:
                player_one.life += 1

    enemy_collide = pygame.sprite.spritecollide(player_one, enemy_group, False)


    if len(enemy_collide) > 0:
        player_one.life -= 1
        player_rect.x = const.POS_X
        player_rect.y = const.POS_Y

    player_one.player_movement = [0, 0]
    for event in pygame.event.get():  # event loop
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                player_one.moving_right = True
            if event.key == K_LEFT:
                player_one.moving_left = True
            if event.key == K_UP and player_one.air_timer < const.MAX_AIRTIME:
                player_one.vertical_momentum = -const.JUMP_HEIGHT
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                player_one.moving_right = False
            if event.key == K_LEFT:
                player_one.moving_left = False

    if player_one.life > 0:
        display.blit(player_one.image, (player_rect.x, player_rect.y))

    display.blit(enemy_one.enemy_img, (enemy_rect_one.x, enemy_rect_one.y))
    display.blit(enemy_two.enemy_img, (enemy_rect_two.x, enemy_rect_two.y))
    portal_group.draw((display))
    portal_group.update()
    background.message(str(player_one.life), const.BLACK, const.FONT_SIZE, const.LIFE_COUNT_LOC)

    if player_one.life == 0:
        display.blit(background.lost_img, (100, 10))

    screen.blit(background.pygame.transform.scale(display, const.WINDOW_SIZE), (0, 0))
    background.pygame.display.update()
    clock.tick(const.FPS)

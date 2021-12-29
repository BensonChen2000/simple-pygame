import pygame
import const


class players(pygame.sprite.Sprite):

    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    player_movement = [0, 0]
    moving_right = False
    moving_left = False
    vertical_momentum = 0
    air_timer = 0
    player_rect = None
    life = 1

    def __init__(self, path, pos_x, pos_y, x_size, y_size):
        self.image = pygame.image.load(path)  # .convert()
        self.rect = self.image.get_rect()
        self.player_rect = pygame.Rect(pos_x, pos_y, x_size, y_size)

    def collision_test(self, rect, tiles):
        hit_list = []
        for tile in tiles:
            if rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list

    def move(self, tiles):
        self.collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
        self.player_rect.x += self.player_movement[0]
        hit_list = self.collision_test(self.player_rect, tiles)
        for tile in hit_list:
            if self.player_movement[0] > 0:
                self.player_rect.right = tile.left
                self.collision_types['right'] = True
            elif self.player_movement[0] < 0:
                self.player_rect.left = tile.right
                self.collision_types['left'] = True
        self.player_rect.y += self.player_movement[1]
        hit_list = self.collision_test(self.player_rect, tiles)
        for tile in hit_list:
            if self.player_movement[1] > 0:
                self.player_rect.bottom = tile.top
                self.collision_types['bottom'] = True
            elif self.player_movement[1] < 0:
                self.player_rect.top = tile.bottom
                self.collision_types['top'] = True
        if self.collision_types['top']:
            self.vertical_momentum = 0
        if self.collision_types['bottom']:
            self.air_timer = 0
            self.vertical_momentum = 0
        else:
            self.air_timer += 1
        return self.player_rect

    def movement(self):
        if self.moving_right:
            self.player_movement[0] += const.HORI_VEL
        if self.moving_left:
            self.player_movement[0] -= const.HORI_VEL
        self.player_movement[1] += self.vertical_momentum
        self.vertical_momentum += const.VERT_ACE
        if self.vertical_momentum > const.MAX_VERT_VEL:
            self.vertical_momentum = const.MAX_VERT_VEL

    def player_move(self, tile_rects):
        self.movement()
        player_rect = self.move(tile_rects)
        self.rect.center = (player_rect.centerx, player_rect.centery)
        return player_rect

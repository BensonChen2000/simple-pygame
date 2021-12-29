import pygame, const

display = pygame.Surface(const.SURFACE_SIZE)  # used as the surface for rendering, which is scaled

grass_img = pygame.image.load(const.GRASS_IMG)
dirt_img = pygame.image.load(const.DIRT_IMG)
brick_img = pygame.image.load(const.BRICK_IMG)
life_img = pygame.image.load(const.LIFE_IMG)
portal_img = pygame.image.load(const.PORTAL_IMG)
lost_img = pygame.image.load(const.LOST_IMG)


def message(text, color, size, pos):
    font = pygame.font.SysFont(None, size)
    screen_text = font.render(text, True, color)
    display.blit(screen_text, pos)

class portal (pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = portal_img
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]

def map(path):
    data = open(path, 'r').read().split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))

    display.fill(const.BLUE)  # clear screen by filling it with blue
    display.set_colorkey(const.WHITE)
    tile_rects = []
    y = 0
    for layer in game_map:
        x = 0
        for tile in layer:
            if tile == '1':
                display.blit(dirt_img, (x * const.TILE_SIZE, y * const.TILE_SIZE))
            elif tile == '2':
                display.blit(grass_img, (x * const.TILE_SIZE, y * const.TILE_SIZE))
            elif tile == '3':
                display.blit(brick_img, (x * const.TILE_SIZE, y * const.TILE_SIZE))

            if (tile != '0'):
                tile_rects.append(
                    pygame.Rect(x * const.TILE_SIZE, y * const.TILE_SIZE, const.TILE_SIZE, const.TILE_SIZE))
            x += 1
        y += 1

    display.blit(life_img, const.LIFE_LOC)
    return display, tile_rects

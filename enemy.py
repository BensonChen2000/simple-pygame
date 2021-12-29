import const, pygame

class enemy (pygame.sprite.Sprite):
    enemy_rect = None
    enemy_img = None
    speed = const.ENEMY_SPEED
    vm = 1

    def __init__(self, path, pos_x, pos_y, x_size, y_size):
        super().__init__()
        self.enemy_img = pygame.image.load(path)  # .convert()
        self.enemy_img.set_colorkey(const.BLACK)
        self.enemy_rect = pygame.Rect(pos_x, pos_y, x_size, y_size)
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]

    def collision_x(self, rect, tiles):
        hit_list = []
        for tile in tiles:
            if rect.y - 8 < tile.y < rect.y + 8:
                hit_list.append(tile)
        return hit_list

    def collision_y(self, rect, tiles):
        hit_list = []
        for tile in tiles:
            if rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list

    def move (self, tiles):
        self.enemy_rect.x += self.speed
        self.enemy_rect.y += self.vm
        hit_x = self.collision_x(self.enemy_rect, tiles)
        for t in hit_x:
            if t.colliderect(self.enemy_rect):
                self.speed = -self.speed
        hit_y = self.collision_y(self.enemy_rect, tiles)
        if not hit_y:
            self.speed = -self.speed
        for t in hit_y:
            if self.enemy_rect.colliderect(t):
                self.vm = 0

        return self.enemy_rect

    def update(self, enemy_rect):
        self.rect.center = (enemy_rect.x, enemy_rect.y)

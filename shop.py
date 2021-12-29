import pygame, sys
import const

#shopping = True


# input x&y location of mouse
# make a display of three features + title
# output shop_display, upgrades

def Click_location(pos):
    upgrades = {'Speed Boost': False, 'Jump Boost': False, 'Extra Life': False}
    if const.SHOP_X < pos[0] < const.SHOP_X + const.SHOP_W:
        if const.SHOP_Y < pos[1] < const.SHOP_Y + const.SHOP_H / 3:
            upgrades['Speed Boost'] = True
            return True, upgrades
        elif const.SHOP_Y + const.SHOP_H / 3 < pos[1] < const.SHOP_Y + const.SHOP_H * 2 / 3:
            upgrades['Jump Boost'] = True
            return True, upgrades
        elif const.SHOP_Y + const.SHOP_H * 2 / 3 < pos[1] < const.SHOP_Y + const.SHOP_H:
            upgrades['Extra Life'] = True
            return True, upgrades
    return False, upgrades


def Shop():
    clock = pygame.time.Clock()
    pygame.init()  # initiates pygame
    pygame.display.set_caption('Pygame Platformer', 'r')
    screen = pygame.display.set_mode(const.WINDOW_SIZE)
    shop_display = pygame.Surface((const.SHOP_W, const.SHOP_H))
    FONT = pygame.font.Font(None, const.TEXT_SIZE)
    Color = const.TEXT_COLOR
    item_one_img = pygame.image.load(const.ITEM1_IMAGE)
    item_one_img.set_colorkey(const.BLACK)
    item_two_img = pygame.image.load(const.ITEM2_IMAGE)
    item_three_img = pygame.image.load(const.ITEM3_IMAGE)
    shopping = True

    while shopping:
        screen.fill(const.BLUE)
        shop_display.fill(const.BLUE)
        text_one = FONT.render(const.ITEM_ONE_NAME, True, Color[0])
        text_two = FONT.render(const.ITEM_TWO_NAME, True, Color[1])
        text_three = FONT.render(const.ITEM_THREE_NAME, True, Color[2])
        for event in pygame.event.get():  # event loop
            pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked, upgrades = Click_location(pos)
                if clicked:
                    shopping = False
            if event.type == pygame.MOUSEMOTION:
                clicked, upgrades = Click_location(pos)
                if upgrades['Speed Boost']:
                    Color = [const.BLACK, const.BLACK, const.BLACK]
                    Color[0] = const.WHITE
                elif upgrades['Jump Boost']:
                    Color = [const.BLACK, const.BLACK, const.BLACK]
                    Color[1] = const.WHITE
                elif upgrades['Extra Life']:
                    Color = [const.BLACK, const.BLACK, const.BLACK]
                    Color[2] = const.WHITE
                else:
                    Color = [const.BLACK, const.BLACK, const.BLACK]

        shop_display.blit(item_one_img, (0, 0))
        shop_display.blit(item_two_img, (0, const.SHOP_H / 3))
        shop_display.blit(item_three_img, (0, const.SHOP_H * 2 / 3))
        shop_display.blit(text_one, (const.ITEM_W, const.ITEM_H / 2))
        shop_display.blit(text_two, (const.ITEM_W, const.SHOP_H / 3 + const.ITEM_H / 2))
        shop_display.blit(text_three, (const.ITEM_W, const.SHOP_H * 2 / 3 + const.ITEM_H / 2))
        screen.blit(shop_display, (const.SHOP_X, const.SHOP_Y))

        pygame.display.update()
        clock.tick(const.FPS)
    return upgrades
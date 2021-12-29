"""Python 3.8.5 (v3.8.5:580fbb018f, Jul 20 2020, 12:11:27)
[Clang 6.0 (clang-600.0.57)] on darwin
Type "help", "copyright", "credits" or "license()" for more information."""
import pygame
import pygame.freetype
from pygame.sprite import Sprite
from pygame.rect import Rect
from enum import Enum
from pygame.sprite import RenderUpdates

BLUE = (106, 159, 181)
WHITE = (255, 255, 255)


def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
    """ Returns surface with text written on """
    font = pygame.freetype.SysFont("Courier", font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()


class UIElement(Sprite):
    """ An user interface element that can be added to a surface """

    def __init__(self, center_position, text, font_size, bg_rgb, text_rgb, action=None):
        """
        Args:
            center_position - tuple (x, y)
            text - string of text to write
            font_size - int
            bg_rgb (background colour) - tuple (r, g, b)
            text_rgb (text colour) - tuple (r, g, b)
            action - the gamestate change associated with this button
        """
        self.mouse_over = False

        default_image = create_surface_with_text(
            text=text, font_size=font_size, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        highlighted_image = create_surface_with_text(
            text=text, font_size=font_size * 1.2, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        self.images = [default_image, highlighted_image]

        self.rects = [
            default_image.get_rect(center=center_position),
            highlighted_image.get_rect(center=center_position),
        ]

        self.action = action

        super().__init__()

    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]

    def update(self, mouse_pos, mouse_up):
        """ Updates the mouse_over variable and returns the button's
            action value when clicked.
        """
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                return self.action
        else:
            self.mouse_over = False

    def draw(self, surface):
        """ Draws element onto a surface """
        surface.blit(self.image, self.rect)


class Player:
    """ Stores information about a player """

    def __init__(self, score=0, lives=3, current_level=1):
        self.score = score
        self.lives = lives
        self.current_level = current_level



def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    game_state = GameState.TITLE

    while True:
        if game_state == GameState.TITLE:
            game_state = title_screen(screen)
        if game_state == GameState.NEWGAME:
            player = Player()
            game_state = play_level(screen, player)
        """if game_state == GameState.NEXT_LEVEL:
            player.current_level += 1
            game_state = play_level(screen, player)
        """
        """if game_state == GameState.PLAY:
            player = Player()
            game_state = play_level(screen, player)
        """
        if game_state == GameState.SETTINGS:
            player = Player()
            game_state = settings(screen, player)
        if game_state == GameState.QUIT:
            pygame.quit()
            return


def title_screen(screen):
    start_btn = UIElement(
        center_position=(400, 300),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Start",
        action=GameState.NEWGAME,
    )
    quit_btn = UIElement(
        center_position=(400, 500),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Quit",
        action=GameState.QUIT,
    )
    settings_btn = UIElement(
        center_position=(400, 400),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Settings",
        action=GameState.SETTINGS
    )
    buttons = RenderUpdates(start_btn, quit_btn, settings_btn)

    return game_loop(screen, buttons)


def play_level(screen, player):
    return_btn = UIElement(
        center_position=(140, 570),
        font_size=20,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Return to main menu",
        action=GameState.TITLE,
    )

    play_btn = UIElement(
        center_position=(80, 80),
        font_size=20,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text=f"Level 1",
        #action=GameState.NEXT_LEVEL,
    )

    second_play_btn = UIElement(
        center_position=(220, 80),
        font_size=20,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text=f"Level 2",
        #action=GameState.NEXT_LEVEL,
    )

    buttons = RenderUpdates(return_btn, play_btn, second_play_btn)

    return game_loop(screen, buttons)

def settings(screen, player):
    return_btn = UIElement(
        center_position=(140, 570),
        font_size=20,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Return to main menu",
        action=GameState.TITLE,
    )
    volume_btn = UIElement(
        center_position=(100, 200),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text=f"volume",
        action=GameState.SETTINGS
    )
    developer_btn = UIElement(
        center_position=(300, 400),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text=f"developers: Benson, Henry, Sarah",
        action=GameState.SETTINGS
    )
    buttons = RenderUpdates(return_btn, volume_btn, developer_btn)
    return game_loop(screen, buttons)


def game_loop(screen, buttons):
    """ Handles game loop until an action is return by a button in the
        buttons sprite renderer.
    """
    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        screen.fill(BLUE)

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action

        buttons.draw(screen)
        pygame.display.flip()


class GameState(Enum):
    QUIT = -1
    TITLE = 0
    NEWGAME = 1
    NEXT_LEVEL = 2
    SETTINGS = 4
    PLAY = 3


if __name__ == "__main__":
    main()

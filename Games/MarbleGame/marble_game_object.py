from Games.game_settings import *


class Button:
    def __init__(self, game_display, x, y, width, height, image, action_image, action=None):
        self.game_display = game_display
        mouse_x_pos, mouse_y_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        game_display.blit(image, (x, y))
        if x + width > mouse_x_pos > x and y + height > mouse_y_pos > y:
            game_display.blit(action_image, (x, y))
            if click[0] and action is not None:
                action()
        else:
            game_display.blit(image, (x, y))


def button_1_clicked():
    print(123)


def button_2_clicked():
    print(456)

from Games.game_settings import *


class Button:
    def __init__(self, game_display, x, y, width, height, image, action=None):
        self.game_display = game_display
        mouse_x_pos, mouse_y_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + width > mouse_x_pos > x and y + height > mouse_y_pos > y:
            # image = pygame.transform.scale(image, (x * 0.8, y * 1.05))
            game_display.blit(image, (x, y))
            if click[0] and action is not None:
                action()
        else:
            game_display.blit(image, (x, y))


def button_clicked():
    print(123)

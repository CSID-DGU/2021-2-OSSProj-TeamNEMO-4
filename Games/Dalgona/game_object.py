from Games.game_settings import *


class Dalgona:
    pass


class Point:
    def __init__(self, game_display, x, y, radius):
        self.mouse = pygame.mouse.get_pos()
        self.click = pygame.mouse.get_pressed()
        self.clicked = False
        if x + radius > self.mouse[0] > x - radius and y + radius > self.mouse[1] > y - radius:
            if self.click[0]:
                self.clicked = True

        if self.clicked:
            pygame.draw.circle(game_display, BLACK, [x, y], 6, 5)

        else:
            pygame.draw.circle(game_display, BROWN, [x, y], 6, 2)

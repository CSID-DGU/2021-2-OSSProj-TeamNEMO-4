from Games.game_settings import *


class Dalgona:
    pass


class Point:
    def __init__(self, game_display, x, y, radius):
        self.game_display = game_display
        self.clicked = False
        self.radius = radius
        self.x = x
        self.y = y

    def is_clicked(self):
        mouse = pygame.mouse.get_pos()
        if self.x + self.radius > mouse[0] > self.x - self.radius and self.y + self.radius > \
                mouse[1] > self.y - self.radius:
            if pygame.mouse.get_pressed()[0]:
                self.clicked = True

    def draw(self):
        if self.clicked:
            pygame.draw.circle(self.game_display, BLACK, [self.x, self.y], self.radius, 6)
        else:
            pygame.draw.circle(self.game_display, BROWN, [self.x, self.y], self.radius, 2)

    def punching(self):
        self.is_clicked()
        self.draw()

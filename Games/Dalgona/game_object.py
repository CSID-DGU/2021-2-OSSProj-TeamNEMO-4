import math

from Games.game_settings import *


class Dalgona:
    def __init__(self, width, height, game_screen):
        self.points = []
        for i in range(20):
            theta = (2 * math.pi / 20) * i
            pos_x = width / 2 + 210 * math.cos(theta)
            pos_y = height / 2 + 210 * math.sin(theta)
            self.points.append(Point(game_screen, pos_x, pos_y, 5))

    def draw(self):
        for i in self.points:
            i.punching()

    def checking_success(self):
        is_success = True
        for i in self.points:
            if not i.clicked:
                is_success = False
        return is_success


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

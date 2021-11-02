import math

from Games.game_settings import *


class Dalgona:
    def __init__(self, width, height, game_screen, points_num, shape):
        self.points = []

        if shape == 1:
            for i in range(points_num):
                theta = (2 * math.pi / points_num) * i
                pos_x = width / 2 + 10 + 210 * math.cos(theta)
                pos_y = height / 2 + 210 * math.sin(theta)
                self.points.append(Point(game_screen, pos_x, pos_y, 5))
        elif shape == 2:
            pos_x = width / 2 - 150 - 20
            pos_y = height / 2 - 150 - 20
            for i in range(int(points_num / 4)):
                self.points.append(Point(game_screen, pos_x, pos_y, 5))
                self.points.append(Point(game_screen, pos_x + (width / 2.3), pos_y, 5))
                pos_y += (width / 2.2) / (points_num / 4)
            pos_x = width / 2 - 150 - 20
            pos_y = height / 2 - 150 - 20
            for i in range(int(points_num / 4)):
                self.points.append(Point(game_screen, pos_x, pos_y, 5))
                self.points.append(Point(game_screen, pos_x, pos_y + (width / 2.3), 5))
                pos_x += (width / 2.2) / (points_num / 4)
        elif shape == 3:
            pos_x = width / 2 - 150 - 20
            pos_y = height / 2 - 150 - 20
            for i in range(int(points_num / 4)):
                self.points.append(Point(game_screen, pos_x, pos_y, 5))
                self.points.append(Point(game_screen, pos_x + (width / 2.3), pos_y, 5))
                pos_y += (width / 2.2) / (points_num / 4)
            pos_x = width / 2 - 150 - 20
            pos_y = height / 2 - 150 - 20
            for i in range(int(points_num / 4)):
                self.points.append(Point(game_screen, pos_x, pos_y, 5))
                self.points.append(Point(game_screen, pos_x, pos_y + (width / 2.3), 5))
                pos_x += (width / 2.2) / (points_num / 4)

    def draw(self):
        for i in self.points:
            i.punching()

    def check_win(self):
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

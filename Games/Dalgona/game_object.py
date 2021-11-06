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
                if i % 10 != 0:
                    self.points.append(Point(game_screen, pos_x, pos_y, 5))
                else:
                    self.points.append(Point(game_screen, pos_x, pos_y, 5, wrong_point=True))

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
                if i % 10 != 0:
                    self.points.append(Point(game_screen, pos_x, pos_y, 5))
                    self.points.append(Point(game_screen, pos_x, pos_y + (width / 2.3), 5))
                else:
                    self.points.append(Point(game_screen, pos_x, pos_y, 5, wrong_point=True))
                    self.points.append(Point(game_screen, pos_x, pos_y + (width / 2.3), 5, wrong_point=True))
                pos_x += (width / 2.2) / (points_num / 4)

        elif shape == 3:
            pos_x = width / 2
            pos_y = height / 4 + 10
            # self.points.append(Point(game_screen, pos_x, pos_y, 5))
            for i in range(int(points_num / 3)):
                move = ((5 / 12) * height) / (points_num / 3)
                if i % 10 != 0:
                    self.points.append(Point(game_screen, pos_x + ((i + 1) * move * (1 / math.sqrt(3))), pos_y, 5))
                    self.points.append(Point(game_screen, pos_x - ((i + 1) * move * (1 / math.sqrt(3))), pos_y, 5))
                else:
                    self.points.append(
                        Point(game_screen, pos_x + ((i + 1) * move * (1 / math.sqrt(3))), pos_y, 5, wrong_point=True))
                    self.points.append(
                        Point(game_screen, pos_x - ((i + 1) * move * (1 / math.sqrt(3))), pos_y, 5, wrong_point=True))
                pos_y += move

            pos_y = height * (2 / 3)
            self.points.append(Point(game_screen, pos_x, pos_y, 5))
            for i in range(int(points_num / 6)):
                self.points.append(Point(game_screen, pos_x + (i + 1) * (width / 4 / (points_num / 6)), pos_y, 5))
                self.points.append(Point(game_screen, pos_x - (i + 1) * (width / 4 / (points_num / 6)), pos_y, 5))

        elif shape == 4:
            num_of_side = 12
            points_num_of_side = int(points_num / num_of_side)
            side_length = (width / 2) / 3
            half_side_length = side_length / 2
            ratio = math.sqrt(3)
            center = (width / 2, height / 2)
            pos_x = center[0]
            pos_y = center[1] - (half_side_length * ratio) * 2
            reverse_pos_x = center[0]
            reverse_pos_y = center[1] + (half_side_length * ratio) * 2
            for i in range(points_num_of_side):
                increase = i * ((half_side_length * ratio) / points_num_of_side)
                self.points.append(
                    Point(game_screen, pos_x + increase / ratio, pos_y + increase, 5))
                self.points.append(
                    Point(game_screen, pos_x - increase / ratio,
                          pos_y + i * ((half_side_length * ratio) / points_num_of_side), 5))
                self.points.append(Point(game_screen, reverse_pos_x + increase / ratio, reverse_pos_y - increase, 5))
                self.points.append(Point(game_screen, reverse_pos_x - increase / ratio, reverse_pos_y - increase, 5))

            # 안쪽 경계선 뛰어넘고 그리기
            for i in range(points_num_of_side * 2, points_num_of_side * 3):
                increase = i * ((half_side_length * ratio) / points_num_of_side)
                self.points.append(
                    Point(game_screen, pos_x + increase / ratio, pos_y + increase, 5))
                self.points.append(
                    Point(game_screen, pos_x - increase / ratio,
                          pos_y + i * ((half_side_length * ratio) / points_num_of_side), 5))
                self.points.append(Point(game_screen, reverse_pos_x + increase / ratio, reverse_pos_y - increase, 5))
                self.points.append(Point(game_screen, reverse_pos_x - increase / ratio, reverse_pos_y - increase, 5))

            # 가로줄 그리기
            pos_y += half_side_length * ratio
            reverse_pos_y -= half_side_length * ratio
            for i in range(points_num_of_side):
                if i % 10 != 0:
                    self.points.append(
                        Point(game_screen, pos_x + half_side_length + i * (side_length / points_num_of_side), pos_y, 5))
                    self.points.append(
                        Point(game_screen, pos_x - half_side_length - i * (side_length / points_num_of_side), pos_y, 5))
                    self.points.append(
                        Point(game_screen, reverse_pos_x + half_side_length + i * (side_length / points_num_of_side),
                              reverse_pos_y, 5))
                    self.points.append(
                        Point(game_screen, reverse_pos_x - half_side_length - i * (side_length / points_num_of_side),
                              reverse_pos_y, 5))
                else:
                    # wrong_point 그리기.
                    self.points.append(
                        Point(game_screen, pos_x + half_side_length + i * (side_length / points_num_of_side), pos_y, 5,
                              wrong_point=True))
                    self.points.append(
                        Point(game_screen, pos_x - half_side_length - i * (side_length / points_num_of_side), pos_y, 5,
                              wrong_point=True))
                    self.points.append(
                        Point(game_screen, reverse_pos_x + half_side_length + i * (side_length / points_num_of_side),
                              reverse_pos_y, 5, wrong_point=True))
                    self.points.append(
                        Point(game_screen, reverse_pos_x - half_side_length - i * (side_length / points_num_of_side),
                              reverse_pos_y, 5, wrong_point=True))

    def draw(self):
        for i in self.points:
            i.punching()

    def check_win(self):
        result = {"is_success": True, "wrong_point_clicked": False}
        for i in self.points:
            if not i.clicked and not i.wrong_point:
                result["is_success"] = False
            if i.wrong_point and i.clicked:
                result["wrong_point_clicked"] = True
        return result


class Point:
    def __init__(self, game_display, x, y, radius, wrong_point=False):
        self.game_display = game_display
        self.clicked = False
        self.radius = radius
        self.x = x
        self.y = y
        self.wrong_point = wrong_point

    def is_clicked(self):
        mouse = pygame.mouse.get_pos()
        if self.x + self.radius > mouse[0] > self.x - self.radius and self.y + self.radius > \
                mouse[1] > self.y - self.radius:
            if pygame.mouse.get_pressed()[0]:
                self.clicked = True

    def draw(self):
        if self.clicked and not self.wrong_point:
            pygame.draw.circle(self.game_display, BLACK, [self.x, self.y], self.radius, 6)
        elif not self.clicked and not self.wrong_point:
            pygame.draw.circle(self.game_display, BROWN, [self.x, self.y], self.radius, 2)
        elif not self.clicked and self.wrong_point:
            pygame.draw.circle(self.game_display, RED, [self.x, self.y], self.radius, 6)

    def punching(self):
        self.is_clicked()
        self.draw()

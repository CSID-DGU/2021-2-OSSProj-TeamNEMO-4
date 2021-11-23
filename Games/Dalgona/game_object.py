import random

from Games.Dalgona.constants import *
from Games.game_settings import *

CIRCLE = 1
RECTANGLE = 2
TRIANGLE = 3
STAR = 4
CLICKED_POINT_SIZE = 2
UNCLICKED_POINT_SIZE = 6
POINT_SIZE = 5
WRONG_POINTS_NUM = 10


class Dalgona:
    def __init__(self, width, height, game_screen, points_num, shape):
        self.points = []
        self.wrong_point_indexes = []
        self.half_width = width / 2
        self.half_height = height / 2
        self.rectangle_size = width / POINT_RECTANGLE_RATIO
        self.half_rectangle = self.rectangle_size / 2

        if shape == CIRCLE:
            for i in range(points_num):
                # 원의 방정식 이용한 points 배치.
                theta = get_theta(points_num, i)
                pos_x = self.half_width + (int(width * POINT_CIRCLE_RATIO) * math.cos(theta))
                pos_y = self.half_height + (int(width * POINT_CIRCLE_RATIO) * math.sin(theta))
                # points
                self.points.append(Point(game_screen, pos_x, pos_y, POINT_SIZE))

            self.change_wrong_points()

        elif shape == RECTANGLE:
            pos_x = self.half_width - self.half_rectangle
            pos_y = self.half_height - self.half_rectangle
            # 사각형의 좌측 상단 점에서부터 세로줄을 긋고 다시 돌아와 가로줄을 긋는다.
            for i in range(1, int(points_num / 4)):
                self.points.append(Point(game_screen, pos_x, pos_y, POINT_SIZE))
                self.points.append(Point(game_screen, pos_x + self.rectangle_size, pos_y, POINT_SIZE))
                pos_y += (width / RECTANGLE_SHAPE_SIZE_RATIO) / (points_num / 4)
            pos_x = self.half_width - self.half_rectangle
            pos_y = self.half_height - self.half_rectangle
            for i in range(1, int(points_num / 4)):
                self.points.append(Point(game_screen, pos_x, pos_y, POINT_SIZE))
                self.points.append(Point(game_screen, pos_x, pos_y + self.rectangle_size, POINT_SIZE))
                pos_x += (width / RECTANGLE_SHAPE_SIZE_RATIO) / (points_num / 4)

            self.change_wrong_points()

        elif shape == TRIANGLE:
            pos_x = self.half_width
            pos_y = height / 4 + 10
            for i in range(int(points_num / 3)):
                move = ((5 / 12) * height) / (points_num / 3)
                self.points.append(
                    Point(game_screen, pos_x + ((i + 1) * move * (1 / math.sqrt(3))), pos_y, POINT_SIZE))
                self.points.append(
                    Point(game_screen, pos_x - ((i + 1) * move * (1 / math.sqrt(3))), pos_y, POINT_SIZE))
                pos_y += move

            pos_y = height * (2 / 3)
            self.points.append(Point(game_screen, pos_x, pos_y, 5))
            for i in range(int(points_num / 6.5)):
                self.points.append(
                    Point(game_screen, pos_x + (i + 1) * (width / 4 / (points_num / 6)), pos_y, POINT_SIZE))
                self.points.append(
                    Point(game_screen, pos_x - (i + 1) * (width / 4 / (points_num / 6)), pos_y, POINT_SIZE))

            self.change_wrong_points()

        elif shape == STAR:
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
                    Point(game_screen, pos_x + increase / ratio, pos_y + increase, POINT_SIZE))
                self.points.append(
                    Point(game_screen, pos_x - increase / ratio,
                          pos_y + i * ((half_side_length * ratio) / points_num_of_side), POINT_SIZE))
                self.points.append(Point(game_screen, reverse_pos_x + increase / ratio, reverse_pos_y - increase, 5))
                self.points.append(Point(game_screen, reverse_pos_x - increase / ratio, reverse_pos_y - increase, 5))

            # 안쪽 경계선 뛰어넘고 그리기
            for i in range(points_num_of_side * 2, points_num_of_side * 3):
                increase = i * ((half_side_length * ratio) / points_num_of_side)
                self.points.append(
                    Point(game_screen, pos_x + increase / ratio, pos_y + increase, POINT_SIZE))
                self.points.append(
                    Point(game_screen, pos_x - increase / ratio,
                          pos_y + i * ((half_side_length * ratio) / points_num_of_side), POINT_SIZE))
                self.points.append(
                    Point(game_screen, reverse_pos_x + increase / ratio, reverse_pos_y - increase, POINT_SIZE))
                self.points.append(
                    Point(game_screen, reverse_pos_x - increase / ratio, reverse_pos_y - increase, POINT_SIZE))

            # 가로줄 그리기
            pos_y += half_side_length * ratio
            reverse_pos_y -= half_side_length * ratio
            for i in range(points_num_of_side):
                self.points.append(
                    Point(game_screen, pos_x + half_side_length + i * (side_length / points_num_of_side), pos_y,
                          POINT_SIZE))
                self.points.append(
                    Point(game_screen, pos_x - half_side_length - i * (side_length / points_num_of_side), pos_y,
                          POINT_SIZE))
                self.points.append(
                    Point(game_screen, reverse_pos_x + half_side_length + i * (side_length / points_num_of_side),
                          reverse_pos_y, 5))
                self.points.append(
                    Point(game_screen, reverse_pos_x - half_side_length - i * (side_length / points_num_of_side),
                          reverse_pos_y, 5))
            self.change_wrong_points()

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

    # change wrong point randomly
    def change_wrong_points(self):
        if self.wrong_point_indexes:
            # 이미 wrong points 가 존재할 경우, 리스트에서 제거 후 일반 point 로 변환.
            for i in self.wrong_point_indexes:
                self.points[i].wrong_point = False
            self.wrong_point_indexes.clear()
        wrong_points = random.sample(self.points, WRONG_POINTS_NUM)
        print(wrong_points)
        for point in wrong_points:
            if type(point) is not int:
                point.clicked = False
                point.wrong_point = True
                index = self.points.index(point)
                wrong_points.append(index)


class Point:
    def __init__(self, game_display, x, y, radius, wrong_point=False):
        self.game_display = game_display
        self.clicked = False
        self.radius = radius
        self.x = x
        self.y = y
        self.wrong_point = wrong_point

    def is_clicked(self):
        mouse_x_pos = pygame.mouse.get_pos()[0]
        mouse_y_pos = pygame.mouse.get_pos()[1]

        if self.x + self.radius > mouse_x_pos > self.x - self.radius and self.y + self.radius > \
                mouse_y_pos > self.y - self.radius:
            # 마우스가 point 의 범위 내에서 클릭되었으면 clicked = True 로 설정.
            if pygame.mouse.get_pressed()[0]:
                self.clicked = True

    def draw(self):
        if self.clicked and not self.wrong_point:
            pygame.draw.circle(self.game_display, BLACK, [self.x, self.y], self.radius, UNCLICKED_POINT_SIZE)
        elif not self.clicked and not self.wrong_point:
            pygame.draw.circle(self.game_display, BROWN, [self.x, self.y], self.radius, CLICKED_POINT_SIZE)
        elif not self.clicked and self.wrong_point:
            pygame.draw.circle(self.game_display, RED, [self.x, self.y], self.radius, UNCLICKED_POINT_SIZE)

    def punching(self):
        self.is_clicked()
        self.draw()

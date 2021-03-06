import math

CIRCLE_SHAPE_SIZE_RATIO = 0.275
SHAPE_WIDTH_RATIO = 0.01875
POINT_CIRCLE_RATIO = 0.2625
POINT_RECTANGLE_RATIO = 2.3
RECTANGLE_SHAPE_SIZE_RATIO = 2.2
RECTANGLE_BORDER_RADIUS = 10
WRONG_POINT_INTERVAL = 10
TRIANGLE_ERROR = 5


def get_theta(points_num, i):
    return (2 * math.pi / points_num) * i

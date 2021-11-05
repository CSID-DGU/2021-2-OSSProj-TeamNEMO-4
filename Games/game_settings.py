import random

import pygame

# 화면 속성

SCREEN_TITLE = '오징어 게임'
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

# 색
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
PINK = (227, 62, 126)
YELLOW_BROWN = (207, 153, 59)
BROWN = (117, 48, 0)
DARK_BROWN = (175, 118, 43)

# 시간
TICK_RATE = 120  # FPS
clock = pygame.time.Clock()
pygame.font.init()

# 폰트
large_font = pygame.font.SysFont('comicsans', 75)
STOP_font = pygame.font.SysFont('comicsans', 120)
level_font = pygame.font.SysFont('calibri', 30)
korean_font = pygame.font.Font('../../Font/Pretendard-Medium.otf', 60)
korean_font_small_size = pygame.font.Font('../../Font/Pretendard-Light.otf', 30)
level_font.set_bold(True)


# 메세지 작성 함수들
def text_objects(text, color, text_font):
    textSurface = text_font.render(text, True, color).convert_alpha()
    return textSurface, textSurface.get_rect()


def message_to_screen_center(surface, msg, color, text_font, y, ref_w, ref_h):
    textSurf, textRect = text_objects(msg, color, text_font)
    cur_w, cur_h = surface.get_size()
    txt_w, txt_h = textSurf.get_size()
    textSurf = pygame.transform.smoothscale(textSurf, (txt_w * cur_w // ref_w, txt_h * cur_h // ref_h))
    textRect = textSurf.get_rect()
    textRect.center = surface.get_width() / 2, y
    surface.blit(textSurf, textRect)


def message_to_screen_left(surface, msg, color, text_font, x, y, ref_w, ref_h):
    textSurf, textRect = text_objects(msg, color, text_font)
    cur_w, cur_h = surface.get_size()
    txt_w, txt_h = textSurf.get_size()
    textSurf = pygame.transform.smoothscale(textSurf, (txt_w * cur_w // ref_w, txt_h * cur_h // ref_h))
    textRect = textSurf.get_rect()
    textRect.center = x, y
    surface.blit(textSurf, textRect)


# 게임 공통 구성요소
# 타이머
class GameOverTimer:

    def __init__(self, timer_time):
        self.start_ticks = pygame.time.get_ticks()
        self.timer_time = timer_time

    def time_checker(self):
        elapsed_time = (pygame.time.get_ticks() - self.start_ticks) / 1000
        timer = round(float(self.timer_time - elapsed_time), 1)
        return timer


# 유저명
# 점수
SCORE = 0


class GameObject:

    def __init__(self, x, y, width, height):
        self.x_pos = x
        self.y_pos = y
        self.width = width
        self.height = height

    def sprite_image(self, image_path):
        object_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(object_image, (self.width, self.height))

    def draw(self, background):
        background.blit(self.image, (self.x_pos, self.y_pos))


class NPC(GameObject):
    BASE_SPEED = 3

    # True  = right, False = Left

    def __init__(self, x, y, width, height, kind_of_npc=1):
        super().__init__(x, y, width / 2, height)  # 범위 보정
        if kind_of_npc == 1:
            object_image = pygame.image.load('common_images/NPC1.png')
        # elif kind_of_npc == 2:
        #     object_image = pygame.image.load('common_images/NPC2.png')
        # else:
        #     object_image = pygame.image.load('common_images/NPC3.png')
        self.go_forward = False
        self.direction = 1
        # 1 right 2 left 3 up 4 down
        self.image = pygame.transform.scale(object_image, (width * (3 / 4), height))

    def draw(self, background):
        if self.go_forward:
            background.blit(self.image, (self.x_pos, self.y_pos))
        else:
            background.blit(pygame.transform.flip(
                self.image, 1, 0), (self.x_pos, self.y_pos))

    def move(self, max_width):
        if self.x_pos <= 0:
            self.direction = 1
        elif self.x_pos >= max_width:
            self.direction = 2
        elif self.y_pos <= 0:
            self.direction = 4
        elif self.y_pos >= max_width:
            self.direction = 3

        if self.direction == 1:
            self.x_pos += self.BASE_SPEED
            self.go_forward = False
        elif self.direction == 2:
            self.x_pos -= self.BASE_SPEED
            self.go_forward = True
        elif self.direction == 3:
            self.y_pos -= self.BASE_SPEED
        else:
            self.y_pos += self.BASE_SPEED

    def change_direction(self):
        self.direction = random.randrange(1, 5)

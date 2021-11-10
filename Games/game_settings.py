import os

import pygame

# 절대경로 변경 함수
def get_abs_path(path):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), path)

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

KOREAN_FONT_PATH = 'Font/Pretendard-Medium.otf'
KOREAN_SMALL_FONT_PATH = 'Font/Pretendard-Light.oft'

large_font = pygame.font.SysFont('comicsans', 75)
STOP_font = pygame.font.SysFont('comicsans', 120)
level_font = pygame.font.SysFont('calibri', 30)
korean_font = pygame.font.Font(os.path.join(os.getcwd(), KOREAN_FONT_PATH), 60)
korean_font_small_size = pygame.font.Font(get_abs_path(KOREAN_SMALL_FONT_PATH), 30)
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


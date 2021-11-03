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
    textSurface = text_font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def message_to_screen_center(surface, msg, color, text_font, y):
    textSurf, textRect = text_objects(msg, color, text_font)
    textRect.center = SCREEN_WIDTH / 2, y
    surface.blit(textSurf, textRect)


def message_to_screen_left(surface, msg, color, font, x, y):
    textSurf, textRect = text_objects(msg, color, font)
    surface.blit(textSurf, (x, y))


# 게임 공통 구성요소
# 타이머
class GameOverTimer:
    start_ticks = pygame.time.get_ticks()

    def __init__(self, timer_time):
        self.timer_time = timer_time

    def time_checker(self):
        elapsed_time = (pygame.time.get_ticks() - self.start_ticks) / 1000
        timer = round(float(self.timer_time - elapsed_time), 1)
        return timer

    def reset_timer(self):
        self.start_ticks = pygame.time.get_ticks()


# 유저명
# 점수
SCORE = 0

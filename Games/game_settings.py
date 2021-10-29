import pygame

# Screen properties
SCREEN_TITLE = '오징어 게임'
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
PINK = (227, 62, 126)
# Clock of game
clock = pygame.time.Clock()
pygame.font.init()
# Initiate fonts
large_font = pygame.font.SysFont('comicsans', 75)
STOP_font = pygame.font.SysFont('comicsans', 120)
level_font = pygame.font.SysFont('calibri', 30)
korean_font = pygame.font.Font('../../Font/Pretendard-Medium.otf', 60)
korean_font_small_size = pygame.font.Font('../../Font/Pretendard-Light.otf', 30)
level_font.set_bold(True)


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

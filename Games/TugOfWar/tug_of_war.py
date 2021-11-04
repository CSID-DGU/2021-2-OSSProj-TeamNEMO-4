import pygame
import sys
import random

# Screen properties
SCREEN_TITLE = '오징어 게임'
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
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


#################실행 부분#################

#파이게임 초기화
pygame.init()

#시작화면 설정
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption(SCREEN_TITLE)
screen.fill(WHITE)
message_to_screen_center(screen, '줄다리기 게임', BLUE, korean_font, SCREEN_HEIGHT/4)
message_to_screen_left(screen, '[조작법]', BLACK, korean_font_small_size, 150, 300)
message_to_screen_left(screen, 'A 클릭하여 줄 당기기', BLACK, korean_font_small_size, 150, 350)
message_to_screen_left(screen, 'D 클릭하여 버티기', BLACK, korean_font_small_size, 150, 400)
message_to_screen_left(screen, 'E 로 시작, Q로 종료', BLACK, korean_font_small_size, 150, 500)

#생성된 창에 설정된 값 표기 ~> 창 업데이트
pygame.display.flip()
running = True

while running:

    clock.tick(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            elif event.key == pygame.K_e:
                run_game_loop(1)




#파이게임 종료
pygame.quit()

import pygame
import sys
import random

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
BLINK = [(224, 255, 255), (192, 240, 255), (128, 224, 255), (64, 192, 255), (128, 224, 255), (192, 240, 255)]
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
# 이미지 로딩
imgBG = pygame.image.load("bg/bg.png")


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


def draw_text(bg, txt, x, y, fnt, col):  # 그림자 포함한 문자 표시
    sur = fnt.render(txt, True, BLACK)
    bg.blit(sur, [x + 1, y + 2])
    sur = fnt.render(txt, True, col)
    bg.blit(sur, [x, y])


# 변수 선언
tmr = 0  # 게임 진행 관리 타이머 변수
time = 121
cball = 10
ball = 10
ballcnt = 0
level = 0
idx = 0  # 게임 진행 관리 인덱스


def main():
    global tmr, time, cball, ball, ballcnt, idx, level
    pygame.init()
    pygame.display.set_caption(SCREEN_TITLE)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # clock=pygame.time.Clock()
    font = korean_font_small_size
    font2 = korean_font
    temp = 0
    cballcnt = random.randint(1, 10)

    try:
        pygame.mixer.music.load("sound/bgm.mp3")
    except:
        print("ogg 파일이 맞지 않거나, 오디오 기기가 접속되어 있지 않습니다")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        tmr = tmr + 1

        key = pygame.key.get_pressed()

        if idx == 0:  # 타이틀 화면
            screen.fill(BLACK)
            draw_text(screen, "Press Space Key", 300, 560, font, BLINK[tmr % 6])
            if key[pygame.K_SPACE] == 1:
                idx = 10

        if idx == 10:
            screen.blit(imgBG, [0, 0])
            minute = int(time / 60)
            second = int(time % 60)
            #if pygame.mixer.music.get_busy() == False:
            #    pygame.mixer.music.play(-1)
            if key[pygame.K_UP] and ballcnt < ball:
                ballcnt += 1
            if key[pygame.K_DOWN] and ballcnt > 0:
                ballcnt -= 1
            if temp == 1 and cball > 1:
                cballcnt = random.randint(1, cball)
                ballcnt = 0
                temp = 0

            time -= 0.1
            txt = font.render("홀짝 게임 " + str(minute) + "분" + str(second) + "초", True, WHITE)

            if key[pygame.K_LEFT]:
                if cballcnt % 2 == 0:
                    ball -= ballcnt
                    cball += ballcnt
                else:
                    ball += ballcnt
                    cball -= ballcnt
                temp = 1

            if key[pygame.K_RIGHT]:
                if cballcnt % 2 == 1:
                    ball -= ballcnt
                    cball += ballcnt
                else:
                    ball += ballcnt
                    cball -= ballcnt
                temp = 1

            pball = font.render("구슬 배팅 : " + str(ballcnt), True, WHITE)
            pball2 = font.render("구슬 개수 : " + str(ball), True, WHITE)
            cballtxt = font.render("상대 구슬 개수 : " + str(cball), True, WHITE)
            cballtxt2 = font.render("상대 배팅 : " + str(cballcnt), True, WHITE)
            # screen.fill(BLACK)

            screen.blit(cballtxt, [570, 50])
            screen.blit(txt, [300, 0])
            screen.blit(pball, [320, 600])
            screen.blit(pball2, [0, 50])
            screen.blit(cballtxt2, [320, 100])
            if ball <= 0:
                idx = 13
            if cball <= 0:
                idx = 11
        if idx == 11:
            screen.fill(BLACK)
            draw_text(screen, "YOU WIN! LEVEL UP!", 250, 560, font, BLINK[tmr % 6])

            if key[pygame.K_SPACE] == 1:
                tmr = 0
                level += 1
                time = 121
                cball = 10
                ball = 10 - level
                ballcnt = 0
                idx = 10
            if ball <= 5:
                idx = 12
        if idx == 12:
            #pygame.mixer.music.stop()
            screen.fill(BLACK)
            draw_text(screen, "THANK YOU FOR PLAYING", 30, 250, font2, BLINK[tmr % 6])
            if key[pygame.K_RETURN] == 1:
                tmr = 0
                level = 0
                time = 121
                cball = 10
                ball = 10
                ballcnt = 0
                idx = 0
        if idx == 13:
            #pygame.mixer.music.stop()
            screen.fill(BLACK)
            draw_text(screen, "GAME OVER", 220, 250, font2, BLINK[tmr % 6])
            if key[pygame.K_RETURN] == 1:
                tmr = 0
                level = 0
                time = 121
                cball = 10
                ball = 10
                ballcnt = 0
                idx = 0
        pygame.display.update()
        clock.tick(10)


if __name__ == '__main__':
    main()
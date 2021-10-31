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
cbead = 10
bead = 10
beadcnt = 0
level = 0
idx = 0  # 게임 진행 관리 인덱스


def main():
    global tmr, time, cbead, bead, beadcnt, idx, level
    pygame.init()
    pygame.display.set_caption(SCREEN_TITLE)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # clock=pygame.time.Clock()
    font = korean_font_small_size
    font2 = korean_font
    temp = 0
    cbeadcnt = random.randint(1, 10)

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
            message_to_screen_center(screen, '홀짝 게임', PINK, korean_font, 100)
            message_to_screen_center(screen, '[ 조작법 ]', PINK, korean_font_small_size, 250)
            message_to_screen_center(screen, '상하 방향키로 구슬 선택', PINK, korean_font_small_size, 350)
            message_to_screen_center(screen, '좌우 방향키로 홀짝 선택', PINK, korean_font_small_size, 450)
            draw_text(screen, "Press Space Key", 300, 560, font, BLINK[tmr % 6])
            if key[pygame.K_SPACE] == 1:
                idx = 10

        if idx == 10:
            screen.blit(imgBG, [0, 0])
            minute = int(time / 60)
            second = int(time % 60)
            #파이참에서 미디어 재생 오류 발생으로 밑에 두 줄 주석처리
            #if pygame.mixer.music.get_busy() == False:
            #    pygame.mixer.music.play(-1)
            if key[pygame.K_UP] and beadcnt < bead:
                beadcnt += 1
            if key[pygame.K_DOWN] and beadcnt > 0:
                beadcnt -= 1
            if temp == 1 and cbead > 1:
                cbeadcnt = random.randint(1, cbead)
                beadcnt = 0
                temp = 0

            time -= 0.1
            txt = font.render("홀짝 게임 " + str(minute) + "분" + str(second) + "초", True, WHITE)

            if key[pygame.K_LEFT]:
                if cbeadcnt % 2 == 0:
                    bead -= beadcnt
                    cbead += beadcnt
                else:
                    bead += beadcnt
                    cbead -= beadcnt
                temp = 1

            if key[pygame.K_RIGHT]:
                if cbeadcnt % 2 == 1:
                    bead -= beadcnt
                    cbead += beadcnt
                else:
                    bead += beadcnt
                    cbead -= beadcnt
                temp = 1

            pbead = font.render("구슬 배팅 : " + str(beadcnt), True, WHITE)
            pbead2 = font.render("구슬 개수 : " + str(bead), True, WHITE)
            cbeadtxt = font.render("상대 구슬 개수 : " + str(cbead), True, WHITE)
            cbeadtxt2 = font.render("상대 배팅 : " + str(cbeadcnt), True, WHITE)
            # screen.fill(BLACK)

            screen.blit(cbeadtxt, [570, 50])
            screen.blit(txt, [300, 0])
            screen.blit(pbead, [320, 600])
            screen.blit(pbead2, [0, 50])
            screen.blit(cbeadtxt2, [320, 100])
            if bead <= 0:
                idx = 13
            if cbead <= 0:
                idx = 11
        if idx == 11:
            screen.fill(BLACK)
            draw_text(screen, "YOU WIN! LEVEL UP!", 250, 560, font, BLINK[tmr % 6])

            if key[pygame.K_SPACE] == 1:
                tmr = 0
                level += 1
                time = 121
                cbead = 10
                bead = 10 - level
                beadcnt = 0
                idx = 10
            if bead <= 5:
                idx = 12
        if idx == 12:
            pygame.mixer.music.stop()
            screen.fill(BLACK)
            draw_text(screen, "THANK YOU FOR PLAYING", 30, 250, font2, BLINK[tmr % 6])
            draw_text(screen, "Press Enter or Return Key", 230, 560, font, BLINK[tmr % 6])
            if key[pygame.K_RETURN] == 1:
                tmr = 0
                level = 0
                time = 121
                cbead = 10
                bead = 10
                beadcnt = 0
                idx = 0
        if idx == 13:
            pygame.mixer.music.stop()
            screen.fill(BLACK)
            draw_text(screen, "GAME OVER", 220, 250, font2, BLINK[tmr % 6])
            draw_text(screen, "Press Enter or Return Key", 230, 560, font, BLINK[tmr % 6])
            if key[pygame.K_RETURN] == 1:
                tmr = 0
                level = 0
                time = 121
                cbead = 10
                bead = 10
                beadcnt = 0
                idx = 0
        pygame.display.update()
        clock.tick(10)


if __name__ == '__main__':
    main()
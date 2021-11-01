import sys
import random
from Games.game_settings import *

class Txt:
    def draw_text(self,bg, txt, x, y, fnt, col):  # 그림자 포함한 문자 표시
        sur = fnt.render(txt, True, BLACK)
        bg.blit(sur, [x + 1, y + 2])
        sur = fnt.render(txt, True, col)
        bg.blit(sur, [x, y])

class Game:
    def main(self):
        self.game_over_timer = GameOverTimer(10)
        # 변수 선언
        BLINK = [(224, 255, 255), (192, 240, 255), (128, 224, 255), (64, 192, 255), (128, 224, 255), (192, 240, 255)]
        tmr = 0
        time = 30
        cbead = 10
        bead = 10
        beadcnt = 0
        level = 0
        idx = 0
        TF = True;
        # 이미지 로딩
        imgBG = pygame.image.load("bg/bg.png")
        imgTrue = pygame.image.load("imgs/True.png")
        imgFalse = pygame.image.load("imgs/False.png")

        #global tmr, time, cbead, bead, beadcnt, idx, level
        pygame.init()
        pygame.display.set_caption(SCREEN_TITLE)
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        # clock=pygame.time.Clock()
        font = korean_font_small_size
        font2 = korean_font
        temp = 0
        beadtemp = 0
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
            left_time = self.game_over_timer.time_checker()
            tmr = tmr + 1

            key = pygame.key.get_pressed()

            if idx == 0:  # 타이틀 화면
                screen.fill(BLACK)
                message_to_screen_center(screen, '홀짝 게임', PINK, korean_font, 100)
                message_to_screen_center(screen, '[ 조작법 ]', PINK, korean_font_small_size, 250)
                message_to_screen_center(screen, '상하 방향키로 구슬 선택', PINK, korean_font_small_size, 350)
                message_to_screen_center(screen, '좌우 방향키로 홀짝 선택', PINK, korean_font_small_size, 450)
                Txt.draw_text(self,screen, "Press Space Key", 300, 560, font, BLINK[tmr % 6])
                if key[pygame.K_SPACE] == 1:
                    idx = 10

            if idx == 10:
                screen.blit(imgBG, [0, 0])
                minute = int(time / 60)
                second = int(time % 60)
                if left_time<=0 :
                    idx = 13
                if pygame.mixer.music.get_busy() == False:
                    pygame.mixer.music.play(-1)
                if key[pygame.K_UP] and beadcnt < bead:
                    beadcnt += 1
                if key[pygame.K_DOWN] and beadcnt > 0:
                    beadcnt -= 1
                if beadtemp == 1 and cbead > 1:
                    cbeadcnt = random.randint(1, cbead)
                    beadcnt = 0
                    beadtemp = 0

                time -= 0.1
                #txt = font.render("홀짝 게임 " + str(minute) + "분" + str(second) + "초", True, WHITE)
                txt = font.render("홀짝 게임 " + str(left_time) + "초", True, WHITE)
                if key[pygame.K_LEFT]:
                    if cbeadcnt % 2 == 0:
                        TF = False
                        bead -= beadcnt
                        cbead += beadcnt
                    else:
                        TF = True
                        bead += beadcnt
                        cbead -= beadcnt
                    idx = 14
                    beadtemp = 1
                    temp = tmr

                if key[pygame.K_RIGHT]:
                    if cbeadcnt % 2 == 1:
                        TF = False
                        bead -= beadcnt
                        cbead += beadcnt
                    else:
                        TF = True
                        bead += beadcnt
                        cbead -= beadcnt
                    idx = 14
                    beadtemp = 1
                    temp = tmr

                pbead = font.render("구슬 배팅 : " + str(beadcnt), True, WHITE)
                pbead2 = font.render("구슬 개수 : " + str(bead), True, WHITE)
                cbeadtxt = font.render("상대 구슬 개수 : " + str(cbead), True, WHITE)
                # cbeadtxt2=font.render("상대 배팅 : "+str(cbeadcnt), True, WHITE)
                # screen.fill(BLACK)

                screen.blit(cbeadtxt, [570, 50])
                screen.blit(txt, [300, 0])
                screen.blit(pbead, [320, 600])
                screen.blit(pbead2, [0, 50])
                # screen.blit(cbeadtxt2, [320, 100])

            if idx == 11:
                screen.fill(BLACK)
                Txt.draw_text(self,screen, "YOU WIN! LEVEL UP!", 250, 560, font, BLINK[tmr % 6])

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
                self.game_over_timer.reset_timer()
                pygame.mixer.music.stop()
                screen.fill(BLACK)
                Txt.draw_text(self,screen, "THANK YOU FOR PLAYING", 30, 250, font2, BLINK[tmr % 6])
                if key[pygame.K_RETURN] == 1:
                    tmr = 0  # 게임 진행 관리 타이머 변수
                    level = 0
                    time = 30  # 전체 시간 변수
                    cbead = 10
                    bead = 10
                    beadcnt = 0
                    idx = 0  # 게임 진행 관리 인덱스
            if idx == 13:
                self.game_over_timer.reset_timer()
                pygame.mixer.music.stop()
                screen.fill(BLACK)
                Txt.draw_text(self,screen, "GAME OVER", 220, 250, font2, BLINK[tmr % 6])
                if key[pygame.K_RETURN] == 1:
                    tmr = 0  # 게임 진행 관리 타이머 변수
                    level = 0
                    time = 30  # 전체 시간 변수
                    cbead = 10
                    bead = 10
                    beadcnt = 0
                    idx = 0  # 게임 진행 관리 인덱스
            if idx == 14:
                screen.fill(BLACK)
                if temp <= tmr - 20:
                    if TF:
                        screen.blit(imgTrue, [0, 0])
                        if temp <= tmr - 30:
                            idx = 10
                            if bead <= 0:
                                idx = 13
                            if cbead <= 0:
                                idx = 11

                    else:
                        screen.blit(imgFalse, [0, 0])
                        if temp <= tmr - 30:
                            idx = 10
                            if bead <= 0:
                                idx = 13
                            if cbead <= 0:
                                idx = 11
            pygame.display.update()
            clock.tick(10)

if __name__ == '__main__':
    new_txt=Txt()
    new_game = Game()
    new_game.main()


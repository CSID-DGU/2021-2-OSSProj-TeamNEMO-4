import sys
import random
from Games.game_settings import *

class MarbleGame:
    # 변수 선언
    idx = 0  # 화면 전환 관리 변수 0 : 타이틀
    player_beads = 10
    player_betting = 1
    computer_beads = 2
    computer_betting = random.randint(1, 3)
    marble_game_level = 0
    betting_success = True
    betting_button_pressed = False
    screen_buffer = 0  # 화면 대기 구현 변수
    marble_game_timer = 0
    fail_eff = 0
    fail_eff_x = random.randint(-20, 20)
    fail_eff_y = random.randint(-10, 10)
    xlocation = []  # 추후 상대 위치 리스트 만들기
    ylocation = []  # 추후 상대 위치 리스트 만들기
    score=0
    # 이미지 로딩
    imgBG = pygame.image.load("bg/bg.png")  # 배경 이미지
    imgTrue = pygame.image.load("imgs/True.png")  # 배팅 성공 이미지
    imgFalse = pygame.image.load("imgs/False.png")  # 배팅 실패 이미지

    def __init__(self,width,height):
        pygame.display.set_caption(SCREEN_TITLE)
        self.width = width
        self.height = height
        # Screen set-up
        self.game_screen = pygame.display.set_mode((width, height),pygame.RESIZABLE)
        self.ref_w, self.ref_h = self.game_screen.get_size()
        self.game_screen.fill(PINK)

    def reset_variable(self):
        self.player_beads = 10
        self.player_betting = 1
        self.computer_beads = 10
        self.computer_betting = 0
        self.marble_game_level = 0
        self.marble_game_timer = 0
        self.idx = 0  # 초기 화면으로

    def draw_title(self):
        self.game_screen.fill(PINK)
        message_to_screen_center(self.game_screen, '홀짝 게임', WHITE, korean_font, self.game_screen.get_height() / 4,
                                     self.ref_w, self.ref_h)
        message_to_screen_center(self.game_screen, '[ 조작법 ]', WHITE, korean_font_small_size,
                                     self.game_screen.get_height() / 3, self.ref_w, self.ref_h)
        message_to_screen_center(self.game_screen, '상하 방향키로 구슬 선택', WHITE, korean_font_small_size,
                                     self.game_screen.get_height() / 2, self.ref_w, self.ref_h)
        message_to_screen_center(self.game_screen, '좌우 방향키로 홀짝 선택', WHITE, korean_font_small_size,
                                     self.game_screen.get_height() / 1.5, self.ref_w, self.ref_h)
        message_to_screen_center(self.game_screen, 'Press Space Key', WHITE, korean_font_small_size,
                                     self.game_screen.get_height() / 1.25, self.ref_w, self.ref_h)
        self.score = 0
    def draw_game_over(self):
        pygame.mixer.music.stop()
        self.game_screen.fill(BLACK)
        message_to_screen_center(self.game_screen, "GAME OVER", WHITE, korean_font,
                                 self.game_screen.get_height() / 4, self.ref_w, self.ref_h)
        message_to_screen_center(self.game_screen, 'Press Enter or Return Key', WHITE, korean_font_small_size,
                                 self.game_screen.get_height() / 1.25, self.ref_w, self.ref_h)
        message_to_screen_left(self.game_screen, "SCORE : " + str(self.score), WHITE, korean_font,
                               self.game_screen.get_width() / 2, self.game_screen.get_height() / 2, self.ref_w,
                               self.ref_h)
    def level_up(self):
        self.game_screen.fill(BLACK)
        message_to_screen_center(self.game_screen, 'YOU WIN! LEVEL UP!', WHITE, korean_font,self.game_screen.get_height() / 4, self.ref_w, self.ref_h)
        if self.screen_buffer <= self.marble_game_timer - 20:
            self.marble_game_timer = 0
            self.marble_game_level += 1
            self.player_beads = 10 - self.marble_game_level
            self.player_betting = 1
            self.computer_beads = 10
            self.computer_betting = 0
            self.idx = 1
        if self.player_beads <= 5:  # 플레이어 구슬이 5개 이하라면
            self.idx = 12  # 클리어 화면으로
    def draw_true_false(self):
        self.game_screen.fill(BLACK)
        if self.screen_buffer <= self.marble_game_timer - 20:
            if self.betting_success:
                self.imgTrue = pygame.transform.scale(self.imgTrue, (
                self.game_screen.get_width(), self.game_screen.get_height()))
                self.game_screen.blit(self.imgTrue, [0, 0])
                if self.screen_buffer <= self.marble_game_timer - 30:
                    self.idx = 1
                    if self.player_beads <= 0:
                        self.idx = 13
                    if self.computer_beads <= 0:
                        self.screen_buffer = self.marble_game_timer
                        self.idx = 11
            else:
                self.imgFalse = pygame.transform.scale(self.imgFalse, (
                self.game_screen.get_width(), self.game_screen.get_height()))
                self.game_screen.blit(self.imgFalse, [0, 0])
                if self.fail_eff > 0:
                    self.fail_eff_x = random.randint(-20, 20)
                    self.fail_eff_y = random.randint(-10, 10)
                    self.fail_eff = self.fail_eff - 1
                self.game_screen.blit(self.imgFalse, [self.fail_eff_x, self.fail_eff_y])
                if self.screen_buffer <= self.marble_game_timer - 30:
                    self.idx = 1
                    if self.player_beads <= 0:
                        self.idx = 13
                    if self.computer_beads <= 0:
                        self.screen_buffer = self.marble_game_timer
                        self.idx = 11
    def draw_clear(self):
        pygame.mixer.music.stop()
        self.game_screen.fill(BLACK)
        message_to_screen_center(self.game_screen, "THANK YOU FOR PLAYING", WHITE, korean_font,
                                 self.game_screen.get_height() / 4, self.ref_w, self.ref_h)
        message_to_screen_center(self.game_screen, 'Press Enter or Return Key', WHITE, korean_font_small_size,
                                 self.game_screen.get_height() / 1.25, self.ref_w, self.ref_h)
        self.score=0

    def start_marble_game(self):
        #배경 음악 로딩
        try:
            pygame.mixer.music.load("sound/bgm.mp3")
            beadsound=pygame.mixer.Sound("sound/beadsound.mp3")
            beadsound2=pygame.mixer.Sound("sound/beadsound2.mp3")
        except:
            print("ogg 파일이 맞지 않거나, 오디오 기기가 접속되어 있지 않습니다")

        #게임 루프
        while True:
            self.marble_game_timer+=1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type==pygame.VIDEORESIZE:
                    self.game_screen=pygame.display.set_mode((event.w,event.h),pygame.RESIZABLE)

            key = pygame.key.get_pressed() #모든 키 입력 감지
            if self.idx==0: #0은 타이틀 화면
                self.draw_title()
                if key[pygame.K_SPACE] == 1:
                    game_over_timer = GameOverTimer(60)
                    self.idx = 1  # 스페이스키 입력시 1번 화면으로 이동
            if self.idx==1:
                # 타이머
                left_time = game_over_timer.time_checker()
                self.imgBG=pygame.transform.scale(self.imgBG,(self.game_screen.get_width(),self.game_screen.get_height()))
                self.game_screen.blit(self.imgBG,[0,0])
                if pygame.mixer.music.get_busy() == False: #bgm 재생 정지 상태라면
                    pygame.mixer.music.play(-1) #bgm 재생
                if left_time<=0 :
                    self.idx = 13
                if key[pygame.K_UP] and self.player_betting < self.player_beads and self.player_betting<self.computer_beads: self.player_betting += 1
                if key[pygame.K_DOWN] and self.player_betting > 0: self.player_betting -= 1
                if self.betting_button_pressed == True and self.computer_beads > 1:
                    self.computer_betting = random.randint(1, self.computer_beads)
                    self.player_betting = 1
                    self.betting_button_pressed = False
                if key[pygame.K_LEFT]: #홀 버튼 누름&배팅
                    if self.computer_betting % 2 == 0: #컴퓨터 배팅이 짝이면
                        self.betting_success = False
                        self.player_beads -= self.player_betting
                        self.computer_beads += self.player_betting
                    else:
                        self.betting_success = True
                        self.player_beads += self.player_betting
                        self.computer_beads -= self.player_betting
                        self.score+=self.player_betting
                    self.screen_buffer = self.marble_game_timer
                    self.idx = 14
                    self.fail_eff = 5
                    self.betting_button_pressed = True

                if key[pygame.K_RIGHT]:
                    if self.computer_betting % 2 == 1:
                        self.betting_success = False
                        self.player_beads -= self.player_betting
                        self.computer_beads += self.player_betting
                    else:
                        self.betting_success = True
                        self.player_beads += self.player_betting
                        self.computer_beads -= self.player_betting
                        self.score += self.player_betting
                    self.screen_buffer = self.marble_game_timer
                    self.idx = 14
                    self.fail_eff=5
                    self.betting_button_pressed = True
                if key[pygame.K_RETURN]:
                    if self.computer_betting==2:
                        beadsound.play()
                    elif self.computer_betting==3:
                        beadsound2.play()




                message_to_screen_left(self.game_screen, str(left_time), WHITE, korean_font,
                                       self.game_screen.get_width() / 2, self.game_screen.get_height() / 17, self.ref_w,
                                       self.ref_h)
                message_to_screen_left(self.game_screen, "구슬 개수 : " + str(self.player_beads), WHITE, korean_font_small_size,
                                       self.game_screen.get_width() / 10, self.game_screen.get_height() / 17, self.ref_w,
                                       self.ref_h)
                message_to_screen_left(self.game_screen, "상대 구슬 개수 : " + str(self.computer_beads), WHITE, korean_font_small_size,
                                       self.game_screen.get_width() / 1.2, self.game_screen.get_height() / 17, self.ref_w,
                                       self.ref_h)
                message_to_screen_left(self.game_screen, "배팅 : "+str(self.player_betting), WHITE, korean_font,
                                       self.game_screen.get_width() / 2, self.game_screen.get_height() / 2, self.ref_w,
                                       self.ref_h)
                message_to_screen_left(self.game_screen, "SCORE : " + str(self.score), WHITE, korean_font,
                                       self.game_screen.get_width() / 2, self.game_screen.get_height() / 5, self.ref_w,
                                       self.ref_h)
                message_to_screen_left(self.game_screen, "컴퓨터 배팅 test : " + str(self.computer_betting), WHITE, korean_font,
                                       self.game_screen.get_width() / 2, self.game_screen.get_height() / 7, self.ref_w,
                                       self.ref_h)
            if self.idx == 11:
                self.level_up()
                game_over_timer.reset_timer(10)
            if self.idx == 12: #클리어 화면
                self.draw_clear()
                self.score+=left_time
                game_over_timer.reset_timer(10)
                if key[pygame.K_RETURN] == 1: #엔터 또는 return 키가 눌리면
                    self.reset_variable()
            if self.idx == 13: #게임 오버 화면
                self.draw_game_over()
                if key[pygame.K_RETURN] == 1:
                    game_over_timer.reset_timer(10)
                    self.reset_variable()
            if self.idx == 14: # 홀짝 판정 화면으로
                self.draw_true_false()
            pygame.display.update()
            clock.tick(10)

if __name__ == '__main__':
    pygame.init()
    new_game = MarbleGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    new_game.start_marble_game()

    pygame.quit()
    quit()


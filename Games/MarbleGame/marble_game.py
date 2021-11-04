import sys
import random
from Games.game_settings import *

class MarbleGame:
    # 변수 선언
    idx = 0  # 화면 전환 관리 변수 0 : 타이틀
    player_beads = 10
    player_betting = 1
    computer_beads = 10
    computer_betting = random.randint(1, computer_beads)
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

    def level_up(self):
        self.game_screen.fill(BLACK)
        message_to_screen_center(self.game_screen, 'YOU WIN! LEVEL UP!', WHITE, korean_font,self.game_screen.get_height() / 4, self.ref_w, self.ref_h)
        if MarbleGame.screen_buffer <= MarbleGame.marble_game_timer - 20:
            MarbleGame.marble_game_timer = 0
            MarbleGame.marble_game_level += 1
            MarbleGame.player_beads = 10 - MarbleGame.marble_game_level
            MarbleGame.player_betting = 1
            MarbleGame.computer_beads = 10
            MarbleGame.computer_betting = 0
            MarbleGame.idx = 1
        if MarbleGame.player_beads <= 5:  # 플레이어 구슬이 5개 이하라면
            MarbleGame.idx = 12  # 클리어 화면으로

    def start_marble_game(self):
        # 타이머
        game_over_timer = GameOverTimer(1000)



        #배경 음악 로딩
        try:
            pygame.mixer.music.load("sound/bgm.mp3")
        except:
            print("ogg 파일이 맞지 않거나, 오디오 기기가 접속되어 있지 않습니다")

        #게임 루프
        while True:
            left_time = game_over_timer.time_checker()
            MarbleGame.marble_game_timer+=1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type==pygame.VIDEORESIZE:
                    self.game_screen=pygame.display.set_mode((event.w,event.h),pygame.RESIZABLE)

            key = pygame.key.get_pressed() #모든 키 입력 감지
            if MarbleGame.idx==0: #0은 타이틀 화면
                self.game_screen.fill(PINK)
                message_to_screen_center(self.game_screen,'홀짝 게임',WHITE, korean_font,self.game_screen.get_height()/4,self.ref_w, self.ref_h)
                message_to_screen_center(self.game_screen, '[ 조작법 ]', WHITE, korean_font_small_size, self.game_screen.get_height()/3,self.ref_w, self.ref_h)
                message_to_screen_center(self.game_screen, '상하 방향키로 구슬 선택', WHITE, korean_font_small_size, self.game_screen.get_height()/2,self.ref_w, self.ref_h)
                message_to_screen_center(self.game_screen, '좌우 방향키로 홀짝 선택', WHITE, korean_font_small_size, self.game_screen.get_height()/1.5,self.ref_w, self.ref_h)
                message_to_screen_center(self.game_screen, 'Press Space Key', WHITE, korean_font_small_size, self.game_screen.get_height()/1.25,self.ref_w, self.ref_h)
                if key[pygame.K_SPACE] == 1: MarbleGame.idx = 1 #스페이스키 입력시 1번 화면으로 이동

            if MarbleGame.idx==1:
                MarbleGame.imgBG=pygame.transform.scale(MarbleGame.imgBG,(self.game_screen.get_width(),self.game_screen.get_height()))
                self.game_screen.blit(MarbleGame.imgBG,[0,0])

                if pygame.mixer.music.get_busy() == False: #bgm 재생 정지 상태라면
                    pygame.mixer.music.play(-1) #bgm 재생
                if left_time<=0 :
                    MarbleGame.idx = 13
                if key[pygame.K_UP] and MarbleGame.player_betting < MarbleGame.player_beads: MarbleGame.player_betting += 1
                if key[pygame.K_DOWN] and MarbleGame.player_betting > 0: MarbleGame.player_betting -= 1
                if MarbleGame.betting_button_pressed == True and MarbleGame.computer_beads > 1:
                    MarbleGame.computer_betting = random.randint(1, MarbleGame.computer_beads)
                    MarbleGame.player_betting = 1
                    MarbleGame.betting_button_pressed = False
                if key[pygame.K_LEFT]: #홀 버튼 누름&배팅
                    if MarbleGame.computer_betting % 2 == 0: #컴퓨터 배팅이 짝이면
                        MarbleGame.betting_success = False
                        MarbleGame.player_beads -= MarbleGame.player_betting
                        MarbleGame.computer_beads += MarbleGame.player_betting
                    else:
                        MarbleGame.betting_success = True
                        MarbleGame.player_beads += MarbleGame.player_betting
                        MarbleGame.computer_beads -= MarbleGame.player_betting
                    MarbleGame.screen_buffer = MarbleGame.marble_game_timer
                    MarbleGame.idx = 14
                    MarbleGame.fail_eff = 5
                    MarbleGame.betting_button_pressed = True

                if key[pygame.K_RIGHT]:
                    if MarbleGame.computer_betting % 2 == 1:
                        MarbleGame.betting_success = False
                        MarbleGame.player_beads -= MarbleGame.player_betting
                        MarbleGame.computer_beads += MarbleGame.player_betting
                    else:
                        MarbleGame.betting_success = True
                        MarbleGame.player_beads += MarbleGame.player_betting
                        MarbleGame.computer_beads -= MarbleGame.player_betting
                    MarbleGame.screen_buffer = MarbleGame.marble_game_timer
                    MarbleGame.idx = 14
                    MarbleGame.fail_eff=5
                    MarbleGame.betting_button_pressed = True


                message_to_screen_left(self.game_screen, str(left_time), WHITE, korean_font,
                                       self.game_screen.get_width() / 2, self.game_screen.get_height() / 17, self.ref_w,
                                       self.ref_h)
                message_to_screen_left(self.game_screen, "구슬 개수 : " + str(MarbleGame.player_beads), WHITE, korean_font_small_size,
                                       self.game_screen.get_width() / 10, self.game_screen.get_height() / 17, self.ref_w,
                                       self.ref_h)
                message_to_screen_left(self.game_screen, "상대 구슬 개수 : " + str(MarbleGame.computer_beads), WHITE, korean_font_small_size,
                                       self.game_screen.get_width() / 1.2, self.game_screen.get_height() / 17, self.ref_w,
                                       self.ref_h)
                message_to_screen_left(self.game_screen, "배팅 : "+str(MarbleGame.player_betting), WHITE, korean_font,
                                       self.game_screen.get_width() / 2, self.game_screen.get_height() / 2, self.ref_w,
                                       self.ref_h)
            if MarbleGame.idx == 11:
                self.level_up()
            if MarbleGame.idx == 12: #클리어 화면
                pygame.mixer.music.stop()
                self.game_screen.fill(BLACK)
                message_to_screen_center(self.game_screen, "THANK YOU FOR PLAYING", WHITE, korean_font,
                                         self.game_screen.get_height() / 4, self.ref_w, self.ref_h)
                message_to_screen_center(self.game_screen, 'Press Enter or Return Key', WHITE, korean_font_small_size,
                                         self.game_screen.get_height() / 1.25, self.ref_w, self.ref_h)
                if key[pygame.K_RETURN] == 1: #엔터 또는 return 키가 눌리면
                    MarbleGame.player_beads = 10
                    MarbleGame.player_betting = 1
                    MarbleGame.computer_beads = 10
                    MarbleGame.computer_betting = 0
                    MarbleGame.marble_game_level = 0
                    MarbleGame.marble_game_timer = 0
                    MarbleGame.idx = 0  # 초기 화면으로
            if MarbleGame.idx == 13: #게임 오버 화면
                pygame.mixer.music.stop()
                self.game_screen.fill(BLACK)
                message_to_screen_center(self.game_screen, "GAME OVER", WHITE, korean_font,
                                         self.game_screen.get_height() / 4, self.ref_w, self.ref_h)
                message_to_screen_center(self.game_screen, 'Press Enter or Return Key', WHITE, korean_font_small_size,
                                         self.game_screen.get_height() / 1.25, self.ref_w, self.ref_h)
                if key[pygame.K_RETURN] == 1:
                    MarbleGame.player_beads = 10
                    MarbleGame.player_betting = 1
                    MarbleGame.computer_beads = 10
                    MarbleGame.computer_betting = 0
                    MarbleGame.marble_game_level = 0
                    MarbleGame.marble_game_timer = 0
                    MarbleGame.idx = 0  # 초기 화면으로
            if MarbleGame.idx == 14: # 홀짝 판정 화면으로
                self.game_screen.fill(BLACK)
                if MarbleGame.screen_buffer <= MarbleGame.marble_game_timer - 20:
                    if MarbleGame.betting_success:
                        MarbleGame.imgTrue = pygame.transform.scale(MarbleGame.imgTrue,(self.game_screen.get_width(), self.game_screen.get_height()))
                        self.game_screen.blit(MarbleGame.imgTrue, [0, 0])
                        if MarbleGame.screen_buffer <= MarbleGame.marble_game_timer-30:
                            MarbleGame.idx = 1
                            if MarbleGame.player_beads <= 0 :
                                MarbleGame.idx = 13
                            if MarbleGame.computer_beads <= 0 :
                                MarbleGame.screen_buffer = MarbleGame.marble_game_timer
                                MarbleGame.idx = 11
                    else:
                        MarbleGame.imgFalse = pygame.transform.scale(MarbleGame.imgFalse,(self.game_screen.get_width(), self.game_screen.get_height()))
                        self.game_screen.blit(MarbleGame.imgFalse, [0, 0])
                        if MarbleGame.fail_eff > 0:
                            MarbleGame.fail_eff_x = random.randint(-20, 20)
                            MarbleGame.fail_eff_y = random.randint(-10, 10)
                            MarbleGame.fail_eff = MarbleGame.fail_eff - 1
                        self.game_screen.blit(MarbleGame.imgFalse, [MarbleGame.fail_eff_x, MarbleGame.fail_eff_y])
                        if MarbleGame.screen_buffer <= MarbleGame.marble_game_timer-30:
                            MarbleGame.idx = 1
                            if MarbleGame.player_beads <= 0 :
                                MarbleGame.idx = 13
                            if MarbleGame.computer_beads <= 0 :
                                MarbleGame.screen_buffer = MarbleGame.marble_game_timer
                                MarbleGame.idx = 11
            pygame.display.update()
            clock.tick(10)

if __name__ == '__main__':
    pygame.init()
    new_game = MarbleGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    new_game.start_marble_game()

    pygame.quit()
    quit()


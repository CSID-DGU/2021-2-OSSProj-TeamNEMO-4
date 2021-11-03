import sys
import random
from Games.game_settings import *

class MarbleGame:
    def __init__(self,width,height):
        pygame.display.set_caption(SCREEN_TITLE)
        self.width = width
        self.height = height
        # Screen set-up
        self.game_screen = pygame.display.set_mode((width, height),pygame.RESIZABLE)
        self.ref_w, self.ref_h = self.game_screen.get_size()
        self.game_screen.fill(PINK)


    def start_marble_game(self):
        # 타이머
        game_over_timer = GameOverTimer(1000)

        # 변수 선언
        idx=0 #화면 전환 관리 변수 0 : 타이틀
        player_beads=10
        player_betting=0
        computer_beads=10
        computer_betting=random.randint(1, computer_beads)
        marble_game_level=0
        betting_success=True
        betting_button_pressed=False
        screen_buffer=0 #화면 대기 구현 변수
        marble_game_timer=0
        xlocation=[] #추후 상대 위치 리스트 만들기
        ylocation=[] #추후 상대 위치 리스트 만들기
        PR_ERROR_TEST=True

        # 이미지 로딩
        imgBG = pygame.image.load("bg/bg.png") #배경 이미지
        imgTrue = pygame.image.load("imgs/True.png") #배팅 성공 이미지
        imgFalse = pygame.image.load("imgs/False.png") #배팅 실패 이미지

        #배경 음악 로딩
        try:
            pygame.mixer.music.load("sound/bgm.mp3")
        except:
            print("ogg 파일이 맞지 않거나, 오디오 기기가 접속되어 있지 않습니다")

        #게임 루프
        while True:
            left_time = game_over_timer.time_checker()
            marble_game_timer+=1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type==pygame.VIDEORESIZE:
                    self.game_screen=pygame.display.set_mode((event.w,event.h),pygame.RESIZABLE)

            key = pygame.key.get_pressed() #모든 키 입력 감지
            if idx==0: #0은 타이틀 화면
                self.game_screen.fill(PINK)
                message_to_screen_center(self.game_screen,'홀짝 게임',WHITE, korean_font,self.game_screen.get_height()/4,self.ref_w, self.ref_h)
                message_to_screen_center(self.game_screen, '[ 조작법 ]', WHITE, korean_font_small_size, self.game_screen.get_height()/3,self.ref_w, self.ref_h)
                message_to_screen_center(self.game_screen, '상하 방향키로 구슬 선택', WHITE, korean_font_small_size, self.game_screen.get_height()/2,self.ref_w, self.ref_h)
                message_to_screen_center(self.game_screen, '좌우 방향키로 홀짝 선택', WHITE, korean_font_small_size, self.game_screen.get_height()/1.5,self.ref_w, self.ref_h)
                message_to_screen_center(self.game_screen, 'Press Space Key', WHITE, korean_font_small_size, self.game_screen.get_height()/1.25,self.ref_w, self.ref_h)
                if key[pygame.K_SPACE] == 1: idx = 1 #스페이스키 입력시 1번 화면으로 이동

            if idx==1:
                imgBG=pygame.transform.scale(imgBG,(self.game_screen.get_width(),self.game_screen.get_height()))
                self.game_screen.blit(imgBG,[0,0])

                if pygame.mixer.music.get_busy() == False: #bgm 재생 정지 상태라면
                    pygame.mixer.music.play(-1) #bgm 재생
                if left_time<=0 :
                    idx = 13
                if key[pygame.K_UP] and player_betting < player_beads: player_betting += 1
                if key[pygame.K_DOWN] and player_betting > 0: player_betting -= 1
                if betting_button_pressed == True and computer_beads > 1:
                    computer_betting = random.randint(1, computer_beads)
                    player_betting = 0
                    betting_button_pressed = False
                if key[pygame.K_LEFT]: #홀 버튼 누름&배팅
                    if computer_betting % 2 == 0: #컴퓨터 배팅이 짝이면
                        betting_success = False
                        player_beads -= player_betting
                        computer_beads += player_betting
                    else:
                        betting_success = True
                        player_beads += player_betting
                        computer_beads -= player_betting
                    screen_buffer = marble_game_timer
                    idx = 14
                    betting_button_pressed = True

                if key[pygame.K_RIGHT]:
                    if computer_betting % 2 == 1:
                        betting_success = False
                        player_beads -= player_betting
                        computer_beads += player_betting
                    else:
                        betting_success = True
                        player_beads += player_betting
                        computer_beads -= player_betting
                    screen_buffer = marble_game_timer
                    idx = 14
                    betting_button_pressed = True


                message_to_screen_left(self.game_screen, str(left_time), WHITE, korean_font,
                                       self.game_screen.get_width() / 2, self.game_screen.get_height() / 17, self.ref_w,
                                       self.ref_h)
                message_to_screen_left(self.game_screen, "구슬 개수 : " + str(player_beads), WHITE, korean_font_small_size,
                                       self.game_screen.get_width() / 10, self.game_screen.get_height() / 17, self.ref_w,
                                       self.ref_h)
                message_to_screen_left(self.game_screen, "상대 구슬 개수 : " + str(computer_beads), WHITE, korean_font_small_size,
                                       self.game_screen.get_width() / 1.2, self.game_screen.get_height() / 17, self.ref_w,
                                       self.ref_h)
                message_to_screen_left(self.game_screen, "배팅 : "+str(player_betting), WHITE, korean_font,
                                       self.game_screen.get_width() / 2, self.game_screen.get_height() / 2, self.ref_w,
                                       self.ref_h)
            if idx == 11:
                self.game_screen.fill(BLACK)
                message_to_screen_center(self.game_screen, 'YOU WIN! LEVEL UP!', WHITE, korean_font,
                                         self.game_screen.get_height() / 4, self.ref_w, self.ref_h)
                if screen_buffer <= marble_game_timer - 20:
                    marble_game_timer=0
                    marble_game_level += 1
                    player_beads = 10 - marble_game_level
                    player_betting = 0
                    computer_beads = 10
                    computer_betting = 0
                    idx = 1
                if player_beads <= 5:#플레이어 구슬이 5개 이하라면
                    idx = 12 #클리어 화면으로
            if idx == 12: #클리어 화면
                pygame.mixer.music.stop()
                self.game_screen.fill(BLACK)
                message_to_screen_center(self.game_screen, "THANK YOU FOR PLAYING", WHITE, korean_font,
                                         self.game_screen.get_height() / 4, self.ref_w, self.ref_h)
                message_to_screen_center(self.game_screen, 'Press Enter or Return Key', WHITE, korean_font_small_size,
                                         self.game_screen.get_height() / 1.25, self.ref_w, self.ref_h)
                if key[pygame.K_RETURN] == 1: #엔터 또는 return 키가 눌리면
                    player_beads = 10
                    player_betting = 0
                    computer_beads = 10
                    computer_betting = 0
                    marble_game_level = 0
                    marble_game_timer = 0
                    idx = 0  # 초기 화면으로
            if idx == 13: #게임 오버 화면
                pygame.mixer.music.stop()
                self.game_screen.fill(BLACK)
                message_to_screen_center(self.game_screen, "GAME OVER", WHITE, korean_font,
                                         self.game_screen.get_height() / 4, self.ref_w, self.ref_h)
                message_to_screen_center(self.game_screen, 'Press Enter or Return Key', WHITE, korean_font_small_size,
                                         self.game_screen.get_height() / 1.25, self.ref_w, self.ref_h)
                if key[pygame.K_RETURN] == 1:
                    player_beads = 10
                    player_betting = 0
                    computer_beads = 10
                    computer_betting = 0
                    marble_game_level = 0
                    marble_game_timer = 0
                    idx = 0  # 초기 화면으로
            if idx == 14: # 홀짝 판정 화면으로
                self.game_screen.fill(BLACK)
                if screen_buffer <= marble_game_timer - 20:
                    if betting_success:
                        imgTrue = pygame.transform.scale(imgTrue,(self.game_screen.get_width(), self.game_screen.get_height()))
                        self.game_screen.blit(imgTrue, [0, 0])
                        if screen_buffer <= marble_game_timer-30:
                            idx = 1
                            if player_beads <= 0 :
                                idx = 13
                            if computer_beads <= 0 :
                                screen_buffer = marble_game_timer
                                idx = 11
                    else:
                        imgFalse = pygame.transform.scale(imgFalse,(self.game_screen.get_width(), self.game_screen.get_height()))
                        self.game_screen.blit(imgFalse, [0, 0])
                        if screen_buffer <= marble_game_timer-30:
                            idx = 1
                            if player_beads <= 0 :
                                idx = 13
                            if computer_beads <= 0 :
                                screen_buffer = marble_game_timer
                                idx = 11
            pygame.display.update()
            clock.tick(10)

if __name__ == '__main__':
    pygame.init()
    new_game = MarbleGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    new_game.start_marble_game()

    pygame.quit()
    quit()


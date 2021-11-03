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
        game_over_timer = GameOverTimer(10)

        # 변수 선언
        idx=0 #화면 전환 관리 변수 0 : 타이틀

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
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                #if event.type==pygame.VIDEORESIZE:
                    #self.game_screen=pygame.display.set_mode((event.w,event.h),pygame.RESIZABLE)

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

            pygame.display.update()
            clock.tick(20)
if __name__ == '__main__':
    pygame.init()
    new_game = MarbleGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    new_game.start_marble_game()

    pygame.quit()
    quit()
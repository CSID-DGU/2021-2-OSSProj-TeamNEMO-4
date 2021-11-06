import pygame
import sys
import random
from Games.game_settings import *

class TugOfWar:
    # 변수 선언
    game_time = 20
    click = 0
    click_n = 20
    TIMER_TIME = random.randint(2, 5)
    WIN_LEVEL = 5

    def __init__(self, title, width, height):
        self.title = title
        self.width = width
        self.height = height
        # 이미지 로딩
        self.imgBG = pygame.image.load("Images/TugOfWarBack.png")
        self.char_1 = pygame.image.load("Images/char1.png")
        self.char_2 = pygame.image.load("Images/char2.png")
        # 화면 설정
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        # 타이머
        self.game_over_timer = None
        self.a_timer = False
        self.b_timer = False
        # 클릭 잘못 판별 변수
        self.click_wrong = False

    # 시작화면
    def start_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        return
                    elif event.key == pygame.K_e:
                        self.run_game_loop(1)
            # 배경 설정
            self.screen.fill(WHITE)
            self.screen.blit(self.imgBG, (0, 0))
            # 문구 놓기
            message_to_screen_center(self.screen, '줄다리기 게임', WHITE, korean_font, SCREEN_HEIGHT / 4)
            message_to_screen_left(self.screen, '[조작법]', WHITE, korean_font_small_size, 150, 320)
            message_to_screen_left(self.screen, 'A 클릭하여 줄 당기기', WHITE, korean_font_small_size, 150, 370)
            message_to_screen_left(self.screen, 'D 클릭하여 버티기', WHITE, korean_font_small_size, 150, 420)
            message_to_screen_left(self.screen, 'E 로 시작, Q 또는 Esc로 종료', WHITE, korean_font_small_size, 150, 520)
            pygame.display.update()

    # 성공 화면
    def win_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return True
                    elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        return False
            # 배경 설정
            self.screen.fill(BLACK)
            # 문구 넣기
            message_to_screen_center(self.screen, '줄 다리기 게임을 통과했습니다', BLUE, korean_font, 200)
            message_to_screen_center(self.screen, '시작화면으로 이동 : R', BLUE, korean_font, 300)
            message_to_screen_center(self.screen, '게임 종료 : Q', BLUE, korean_font, 400)
            pygame.display.update()

    # 실패 화면
    def lose_game(self):
        message_to_screen_center(self.screen, '탈 락 하 셨 습 니 다', RED, korean_font, self.width/2)
        pygame.display.update()
        clock.tick(2)

    def game_restart(self):
        self.game_over_timer.reset_timer()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return True
                    elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        return False
            # 배경 넣기
            self.screen.fill(WHITE)
            # 문구 넣기
            message_to_screen_center(self.screen, '시작화면으로 이동 : R', RED, korean_font, 300)
            message_to_screen_center(self.screen, '게임 종료 : Q', RED, korean_font, 400)
            pygame.display.update()

    def run_game_loop(self, level):
        game_over = False
        did_win = True
        nClick = self.click_n*level  # 클릭해야하는 클릭 수
        click = 0   # 현재 클릭 수
        # 캐릭터 불러오기
        char_1 = pygame.image.load("Images/char1.png")
        char_2 = pygame.image.load("Images/char2.png")

        # 게임 종료 타이머 설정
        self.game_over_timer = GameOverTimer(self.game_time)

        print('-----------------------------')
        print('LEVEL : ', level)

        start_ticks = pygame.time.get_ticks()
        while not game_over:
            # 전체 남은 시간
            left_time = self.game_over_timer.time_checker()
            if left_time < 0:
                game_over = True
                did_win = False
                break

            # 배경 다시 설정
            self.screen.fill(WHITE)
            self.screen.blit(self.imgBG, (0, 0))

            # A 누르는 타이머
            elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
            timer = round(float(self.TIMER_TIME - elapsed_time), 1)
            # A 누르는 타이머 돌아갈 때 화면에 시간 표시
            if not self.b_timer:
                message_to_screen_center(self.screen, f'Click A : {timer}', WHITE, level_font, self.width * (1 / 2))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                # A 키 누르는 타이머 돌아갈 때 -> A 누르면 click 올라감, D 누르면 게임 종료
                elif event.type == pygame.KEYDOWN:
                    if timer > 0: # A 누르는 타이머가 돌아갈 때
                        if event.key == pygame.K_a:
                            click += 1
                        elif event.key == pygame.K_d:
                            did_win = False
                            self.b_timer = False
                            self.click_wrong = True
                            break # 잘못 클릭하면 for문 탈출
                    if timer <= 0: # D 누르는 타이머가 돌아갈 때
                        if event.key == pygame.K_d:
                            click += 1
                        elif event.key == pygame.K_a:
                            did_win = False
                            self.b_timer = False
                            self.click_wrong = True
                            break
            # 잘못 클릭했을 때 바로 while문 탈출
            if self.click_wrong:
                break

            # 캐릭터 화면에 표시
            for i in range(0, 211, 70):
                self.screen.blit(char_1, (i, 240))
            for i in range(760, 549, -70):
                self.screen.blit(char_2, (i, 240))
            # LEVEL 화면에 표시
            message_to_screen_left(self.screen, 'LEVEL {}'.format(level), WHITE, level_font, 0, 0)
            # 남은 전체 시간 화면에 표시
            message_to_screen_left(self.screen, 'Left Time : {}'.format(left_time), WHITE, level_font, 0, 35)
            # 남은 클릭 수 화면에 표시
            message_to_screen_center(self.screen, 'Left Click : {}'.format((nClick-click)), WHITE, level_font, 10)

            if timer <= 0:
                self.b_timer = True
                time = random.randint(2, 5)
                time_checker = round(float(time - (timer)*(-1)), 1)
                message_to_screen_center(self.screen,
                                         'CLICK D : {}'.format(time_checker), WHITE, level_font, self.height*(1/2))
                if time_checker <= 0:
                    self.b_timer = False
                    start_ticks = pygame.time.get_ticks()
                    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
                    timer = round(float(self.TIMER_TIME - elapsed_time), 2)
                elif self.click_wrong:
                    break

            # did_win이 True인 상태로 반복문 탈출
            if click == nClick:
                break
            pygame.display.update()
            clock.tick(2)

        if did_win:
            if level >= self.WIN_LEVEL:
                self.win_game()
            else:
                message_to_screen_left(self.screen, 'LEVEL {}'.format(level), WHITE, level_font, 0, 0)
                self.run_game_loop(level + 1)
        elif self.game_restart():
            self.run_game_loop(1)
        else:
            return

pygame.init()
new_game = TugOfWar(SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT)
new_game.start_game()

pygame.quit()
quit()
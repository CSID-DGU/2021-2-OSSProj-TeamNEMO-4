import random
import time

import pygame.time

from Games.game_settings import *

# 이미지 좌표
CHARACTER_LOCATION = 'TugOfWar/Images/TOW_Char.png'
BACKGROUND_LOCATION = 'TugOfWar/Images/TugOfWarBack.png'
RANDOM_NUMBER_FOR_TIMER = random.randint(3, 6)


class TugOfWar:
    # 클래스 변수
    NUMBER_OF_CLICKS_TO_CLEAR = 15  # 승리 조건
    WIN_LEVEL = 5  # LEVEL 5 통과하면 게임 끝
    TOTAL_TIME = 40

    def __init__(self, title, width, height):
        self.title = title
        self.width = width
        self.height = height
        # 화면 설정
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.ref_w, self.ref_h = self.screen.get_size()
        self.screen.fill(WHITE)
        pygame.display.set_caption(title)
        # 이미지 불러오기
        self.char = pygame.image.load(get_abs_path(CHARACTER_LOCATION))
        self.imgBG = pygame.image.load(get_abs_path(BACKGROUND_LOCATION))
        # 타이머 설정
        self.game_over_timer = None
        self.a_TIMER = False

    def start_game(self, level, score):
        # while True:
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             return
        #         elif event.type == pygame.KEYDOWN:
        #             if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
        #                 return
        #             elif event.key == pygame.K_e:
        score = self.run_game_loop(level, score)
        return score
        # 배경 설정
        # self.screen.fill(WHITE)
        # imgBG = pygame.transform.scale(self.imgBG, (self.screen.get_width(), self.screen.get_height()))
        # self.screen.blit(imgBG, (0, 0))
        # # 문구 놓기
        # message_to_screen_center(
        #     self.screen, '줄다리기 게임', WHITE, korean_font,
        #     self.screen.get_height() / 4, self.ref_w, self.ref_h)
        # message_to_screen_center(
        #     self.screen, '[조작법]', WHITE, korean_font_small_size,
        #     self.screen.get_height() / 2.1, self.ref_w, self.ref_h)
        # message_to_screen_center(
        #     self.screen, 'A 클릭하여 줄 당기기', WHITE, korean_font_small_size,
        #     self.screen.get_height() / 1.83, self.ref_w, self.ref_h)
        # message_to_screen_center(
        #     self.screen, 'D 클릭하여 버티기', WHITE, korean_font_small_size,
        #     self.screen.get_height() / 1.66, self.ref_w, self.ref_h)
        # message_to_screen_center(
        #     self.screen, 'E 로 시작, Q 또는 Esc로 종료', WHITE, korean_font_small_size,
        #     self.screen.get_height() / 1.4, self.ref_w, self.ref_h)
        # pygame.display.update()

    # 통과 화면
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
            message_to_screen_center(
                self.screen, '줄 다리기 게임을 통과했습니다', BLUE, korean_font, SCREEN_HEIGHT / 4, self.ref_w, self.ref_h)
            message_to_screen_center(
                self.screen, '시작화면으로 이동 : R', BLUE, korean_font, SCREEN_HEIGHT / 3, self.ref_w, self.ref_h)
            message_to_screen_center(
                self.screen, '게임 종료 : Q', BLUE, korean_font, SCREEN_HEIGHT / 2, self.ref_w, self.ref_h)
            pygame.display.update()

    # 실패 화면
    def lose_game(self):
        game_over_image = pygame.image.load(get_abs_path(GAME_OVER_LOCATION))
        game_over_image = pygame.transform.scale(game_over_image, (self.width, self.height))
        self.screen.blit(game_over_image, (0, 0))
        message_to_screen_center(
            self.screen, '탈 락', RED, korean_font, self.width / 2, self.ref_w, self.ref_h)
        pygame.display.update()
        clock.tick(0.5)

    # LEVEL 통과 함수
    # def level_clear(self):
    #     message_to_screen_center(
    #         self.screen, 'LEVEL CLEAR', BLUE, korean_large_font, self.width / 2, self.ref_w, self.ref_h)
    #     pygame.display.update()

    def game_restart(self):
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
            self.screen.fill(BLACK)
            # 문구 넣기
            message_to_screen_center(
                self.screen, '재시도 : R', RED, korean_font, self.height * 3 / 8, self.ref_w, self.ref_h)
            message_to_screen_center(
                self.screen, '시작화면으로 이동 : Q', RED, korean_font, self.height / 2, self.ref_w, self.ref_h)
            pygame.display.update()

    def run_game_loop(self, level, score):
        game_over = False
        did_win = False
        click_wrong = False
        a_time_init = True
        click = 0
        number_of_clicks_to_clear = level * self.NUMBER_OF_CLICKS_TO_CLEAR
        game_over_click = 2 * number_of_clicks_to_clear  # 클릭해야하는 횟수 이 값 넘기면 게임 오버
        wrong_click_num = 0  # 잘못 클릭한 횟수
        a_time = RANDOM_NUMBER_FOR_TIMER  # A 누를 수 있는 시간
        d_time = RANDOM_NUMBER_FOR_TIMER
        all_left_time = None

        # 게임 오버(전체 시간) 타이머 설정
        self.game_over_timer = GameOverTimer(self.TOTAL_TIME)

        start_ticks = pygame.time.get_ticks()
        a_ticks = pygame.time.get_ticks()

        while not game_over:
            # 게임 오버 타이머 남은 시간
            all_left_time = self.game_over_timer.time_checker()

            # 배경 다시 설정
            self.screen.fill(WHITE)
            imgBG = pygame.transform.scale(self.imgBG, (self.screen.get_width(), self.screen.get_height()))
            self.screen.blit(imgBG, (0, 0))

            # 캐릭터 배치
            imgChar = pygame.transform.scale(self.char, (self.screen.get_width(), self.screen.get_height()))
            # 캐릭터 움직이도록 설정
            self.screen.blit(imgChar, ((number_of_clicks_to_clear - click), 0))

            # d 누르는 타이머 설정
            elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
            d_timer = round(float(d_time - elapsed_time), 1)
            # 현재 레벨, 게임 오버 타이머 화면 좌측 상단에 render
            message_to_screen_left(
                self.screen, 'Level:' + str(level), WHITE, level_font, 70, 30, self.ref_w,
                self.ref_h)
            message_to_screen_left(
                self.screen, "GAME OVER : " + str(all_left_time), WHITE, level_font, 165, 65, self.ref_w,
                self.ref_h)
            message_to_screen_left(
                self.screen, "SCORE : " + str(score), WHITE, level_font, self.width - 130, 40, self.ref_w,
                self.ref_h)
            # 남은 클릭에러 허용 횟수 화면에 표시
            # message_to_screen_left(
            #     self.screen.get_width() / 8, self.screen.get_height() / 8, self.ref_w, self.ref_h)
            # 남은 클릭 수 화면에 표시
            message_to_screen_center(
                self.screen, 'Left Click : {}'.format(int(number_of_clicks_to_clear - click)), WHITE, level_font,
                self.screen.get_height() / 40,
                self.ref_w, self.ref_h)
            # 메세지 표시 when d 누르는 시간일 때
            if d_timer > 0:
                message_to_screen_center(
                    self.screen, "Press D", WHITE, large_font, self.height / 2, self.ref_w, self.ref_h)
                message_to_screen_center(
                    self.screen, f'{d_timer}', WHITE, large_font, self.height / 3, self.ref_w, self.ref_h)

            # a 누르는 시간 (d 누르는 시간 끝남)
            if d_timer <= 0:
                self.a_TIMER = True
                if a_time_init:
                    a_time = RANDOM_NUMBER_FOR_TIMER
                    a_time_init = False
                a_time_checker = round(a_time - (d_timer) * (-1), 1)
                message_to_screen_center(
                    self.screen, "Click A", WHITE, large_font, self.height / 2, self.ref_w, self.ref_h)
                message_to_screen_center(
                    self.screen, f'{a_time_checker}', WHITE, large_font, self.height / 3, self.ref_w, self.ref_h)
                if a_time_checker <= 0:  # a 누르는 시간 끝나면 d 누르는 타이머 초기화
                    self.a_TIMER = False
                    a_time_init = True
                    start_ticks = pygame.time.get_ticks()
                    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
                    d_time = RANDOM_NUMBER_FOR_TIMER
                    d_timer = round(float(d_time - elapsed_time), 1)
                else:
                    a_elapsed_time = (pygame.time.get_ticks() - a_ticks) / 1000
                    a_timer = round(float(a_time - a_elapsed_time), 1)
                    if a_timer <= 0:
                        a_ticks = pygame.time.get_ticks()
                        a_elapsed_time = (pygame.time.get_ticks() - a_ticks) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if d_timer > 0:  # d 누르는 타이머 돌아갈 때
                        if event.key == pygame.K_a:
                            wrong_click_num += 1
                    if d_timer < 0:  # a 누르는 타이머 돌아갈 때
                        if event.key == pygame.K_d:
                            wrong_click_num += 1

            key = pygame.key.get_pressed()
            if d_timer > 0:
                if key[pygame.K_d] is False:
                    click -= 0.1
            elif d_timer < 0:
                if key[pygame.K_a]:  # 수정필요
                    click += 0.15

            # GAME OVER CONDITIONS
            if all_left_time <= 0:
                message_to_screen_center(
                    self.screen, '시간 초과', RED, korean_font_small_size,
                    self.screen.get_height() / 1.7, self.ref_w, self.ref_h)
                self.lose_game()
                did_win = False
                time.sleep(1.5)
                break
            elif (number_of_clicks_to_clear - click) > game_over_click:
                message_to_screen_center(
                    self.screen, '클릭 수 초과', RED, korean_font_small_size,
                    self.screen.get_height() / 1.7, self.ref_w, self.ref_h)
                self.lose_game()
                break

            # 클릭 수 채운 경우 ~> did_win이 True인 상태로 반복문 탈출
            if click >= number_of_clicks_to_clear:
                # self.level_clear()
                # time.sleep(1.5)
                did_win = True
                break
            pygame.display.update()
            clock.tick(120)
        if did_win:
            # if level >= self.WIN_LEVEL:
            #     self.win_game()
            # else:
            message_to_screen_center(self.screen, '통과!', WHITE, korean_font,
                                     self.height / 3,
                                     self.ref_w,
                                     self.ref_h)
            message_to_screen_center(self.screen, '다음 게임은 무궁화 게임입니다. ', WHITE, korean_font,
                                     self.width / 2,
                                     self.ref_w,
                                     self.ref_h)
            pygame.display.update()
            clock.tick(0.5)
            print(all_left_time)
            return all_left_time

        # elif self.game_restart():
        #     self.run_game_loop(1)
        else:
            game_over_image = pygame.image.load(get_abs_path(GAME_OVER_LOCATION))
            game_over_image = pygame.transform.scale(game_over_image, (self.width, self.height))
            self.screen.blit(game_over_image, (0, 0))
            message_to_screen_center(
                self.screen, '탈 락', RED, korean_font, self.width / 2, self.ref_w, self.ref_h)
            pygame.display.update()
            clock.tick(0.5)
            return


def start_game(level, score):
    pygame.init()
    new_game = TugOfWar(SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT)
    score = new_game.start_game(level, score)
    return score

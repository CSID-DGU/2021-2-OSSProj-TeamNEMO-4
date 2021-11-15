import random

import pygame.time

from Games.game_settings import *

# 이미지 좌표
CHARACTER_LOCATION = 'TugOfWar/Images/TOW_Char.png'
BACKGROUND_LOCATION = 'TugOfWar/Images/TugOfWarBack.png'
RANDOM_NUMBER_FOR_TIMER = random.randint(3, 6)
FPS_RATE = 100


class TugOfWar:
    # 클래스 변수
    NUMBER_OF_PRESS_KEY_TO_CLEAR = 50  # 승리 조건
    CONDITION_OF_GAME_OVER = 80
    WIN_LEVEL = 5  # LEVEL 5 통과하면 게임 끝
    TOTAL_TIME = 40
    POWER_OF_ENEMY = 0.1  # 난이도. 상대가 줄을 당기는 힘. 레벨이 곱해져 상승한다.
    MY_POWER = 0.2

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
        self.character = pygame.image.load(get_abs_path(CHARACTER_LOCATION))
        self.background = pygame.image.load(get_abs_path(BACKGROUND_LOCATION))
        # 타이머 설정
        self.game_over_timer = None

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
        # imgBG = pygame.transform.scale(self.background, (self.screen.get_width(), self.screen.get_height()))
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
        hit_time_init = True
        num_of_pressed = 0
        num_of_press_key_to_clear = self.NUMBER_OF_PRESS_KEY_TO_CLEAR
        condition_of_game_over = self.CONDITION_OF_GAME_OVER
        hit_time = RANDOM_NUMBER_FOR_TIMER  # A 누를 수 있는 시간
        hold_time = RANDOM_NUMBER_FOR_TIMER
        left_time = None
        power_of_enemy = level * self.POWER_OF_ENEMY

        # 게임 오버(전체 시간) 타이머 설정
        self.game_over_timer = GameOverTimer(self.TOTAL_TIME)

        start_ticks = pygame.time.get_ticks()
        hit_ticks = pygame.time.get_ticks()

        while not game_over:
            # 게임 오버 타이머 남은 시간
            left_time = self.game_over_timer.time_checker()

            # 배경 다시 설정
            self.screen.fill(WHITE)
            image_background = pygame.transform.scale(self.background,
                                                      (self.screen.get_width(), self.screen.get_height()))
            self.screen.blit(image_background, (0, 0))

            # 캐릭터 배치
            image_character = pygame.transform.scale(self.character,
                                                     (self.screen.get_width(), self.screen.get_height()))
            # 캐릭터 움직이도록 설정
            self.screen.blit(image_character, ((num_of_press_key_to_clear - num_of_pressed), 0))

            # 버티기 타이머
            elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
            hold_timer = round(float(hold_time - elapsed_time), 1)

            # 현재 레벨, 게임 오버 타이머 화면 좌측 상단에 render
            message_to_screen_left(
                self.screen, 'Level : ' + str(level), WHITE, level_font, 70, 30, self.ref_w,
                self.ref_h)
            message_to_screen_left(
                self.screen, "GAME OVER : " + str(left_time), WHITE, level_font, 165, 65, self.ref_w,
                self.ref_h)
            message_to_screen_left(
                self.screen, "SCORE : " + str(score), WHITE, level_font, self.width - 130, 40, self.ref_w,
                self.ref_h)
            message_to_screen_center(
                self.screen, '승리까지 {} M'.format(int(num_of_press_key_to_clear - num_of_pressed)), WHITE,
                korean_font_small_size,
                self.screen.get_height() / 4,
                self.ref_w, self.ref_h)

            # hold time 렌더링
            if hold_timer > 0:
                message_to_screen_center(
                    self.screen, "Space 누르고 버티기", WHITE, korean_font, self.height * (2 / 3), self.ref_w, self.ref_h)

            # hit time
            if hold_timer <= 0:
                if hit_time_init:
                    hit_time = RANDOM_NUMBER_FOR_TIMER
                    hit_time_init = False
                hit_time_checker = round(hit_time - (hold_timer) * (-1), 1)
                message_to_screen_center(
                    self.screen, "← → 연타 !", WHITE, korean_large_font, self.height * (2 / 3), self.ref_w, self.ref_h)

                if hit_time_checker <= 0:  # 연타시간 종료 후 버티기 타이머 재설정.
                    hit_time_init = True
                    start_ticks = pygame.time.get_ticks()
                    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
                    hold_time = RANDOM_NUMBER_FOR_TIMER
                    hold_timer = round(float(hold_time - elapsed_time), 1)
                else:
                    hit_elapsed_time = (pygame.time.get_ticks() - hit_ticks) / 1000
                    hit_timer = round(float(hit_time - hit_elapsed_time), 1)
                    if hit_timer <= 0:
                        hit_ticks = pygame.time.get_ticks()
                        hit_elapsed_time = (pygame.time.get_ticks() - hit_ticks) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            # 줄 당겨지고 당기기
            key = pygame.key.get_pressed()
            if hold_timer > 0:
                if key[pygame.K_SPACE] is False:
                    num_of_pressed -= power_of_enemy
            elif hold_timer < 0:
                if key[pygame.K_RIGHT] is False and key[pygame.K_LEFT] is False:
                    num_of_pressed -= power_of_enemy

                elif key[pygame.K_RIGHT] is True or key[pygame.K_LEFT] is True:
                    num_of_pressed += self.MY_POWER

            # GAME OVER CONDITIONS
            if left_time <= 0:
                message_to_screen_center(
                    self.screen, '시간 초과', RED, korean_font_small_size,
                    self.screen.get_height() / 1.7, self.ref_w, self.ref_h)
                self.lose_game()
                did_win = False
                break
            elif (num_of_press_key_to_clear - num_of_pressed) > condition_of_game_over:
                message_to_screen_center(
                    self.screen, '상대편 승리', RED, korean_large_font,
                    self.height / 2, self.ref_w, self.ref_h)
                pygame.display.update()
                clock.tick(1)
                self.lose_game()
                break
            # 승리조건 만족 -> did_win = True 로 반복문 탈출.
            elif num_of_pressed >= num_of_press_key_to_clear:
                # self.level_clear()
                did_win = True
                break
            pygame.display.update()
            clock.tick(FPS_RATE)

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
            return left_time

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

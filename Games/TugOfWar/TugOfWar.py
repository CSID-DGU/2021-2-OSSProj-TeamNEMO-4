import random

import pygame.time

from Games.game_settings import *

# 이미지 좌표
PULLING_IMG = 'TugOfWar/Images/pulling.png'
HOLDING_IMG = 'TugOfWar/Images/holding.png'
BACKGROUND_LOCATION = 'TugOfWar/Images/TugOfWarBack.png'
# BGM 좌표
BGM_LOCATION = 'TugOfWar/Sound/bgm.mp3'
RANDOM_NUMBER_FOR_TIMER = random.randint(3, 6)
FPS_RATE = 100


class TugOfWar:
    # 클래스 변수
    NUMBER_OF_PRESS_KEY_TO_CLEAR = 50  # 승리 조건
    CONDITION_OF_GAME_OVER = 70
    WIN_LEVEL = 5  # LEVEL 5 통과하면 게임 끝
    TOTAL_TIME = 40
    POWER_OF_ENEMY = 0.1  # 난이도. 상대가 줄을 당기는 힘. 레벨이 곱해져 상승한다.
    MY_POWER = 0.2

    def __init__(self, title, width, height, current_screen):
        self.title = title
        self.width = width
        self.height = height
        # 화면 설정
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.ref_w, self.ref_h = self.screen.get_size()
        self.screen.fill(WHITE)
        pygame.display.set_caption(title)
        # 이미지 불러오기
        self.character_pull = pygame.image.load(get_abs_path(PULLING_IMG))
        self.character_hold = pygame.image.load(get_abs_path(HOLDING_IMG))
        self.background = pygame.image.load(get_abs_path(BACKGROUND_LOCATION))
        # 타이머 설정
        self.game_over_timer = None
        # BGM 넣기
        try:
            pygame.mixer.music.load(get_abs_path(BGM_LOCATION))
        except Exception as e:
            print(e)
            print("사운드 로드 오류")
        pygame.display.set_mode(current_screen, pygame.RESIZABLE)

    def start_game(self, level, score, best_record_mode, select_mode=False):
        score = self.run_game_loop(level, score, best_record_mode, select_mode)
        return score

    def start_game(self, level, score, best_record_mode, select_mode):
        score = self.run_game_loop(level, score, best_record_mode, select_mode)
        return score

    # 통과 화면
    def win_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    return True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        pygame.mixer.music.stop()
                        return True
                    elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        pygame.mixer.music.stop()
                        return False
            # 배경 설정
            self.screen.fill(BLACK)
            # 문구 넣기
            message_to_screen_center(
                self.screen, '줄 다리기 게임을 통과했습니다', BLUE, korean_font, self.screen.get_height() / 4, self.ref_w,
                self.ref_h)
            message_to_screen_center(
                self.screen, '시작화면으로 이동 : R', BLUE, korean_font, self.screen.get_height() / 3, self.ref_w, self.ref_h)
            message_to_screen_center(
                self.screen, '게임 종료 : Q', BLUE, korean_font, self.screen.get_height() / 2, self.ref_w, self.ref_h)
            pygame.display.update()

    # 실패 화면
    def lose_game(self):
        game_over_image = pygame.image.load(get_abs_path(GAME_OVER_LOCATION))
        game_over_image = pygame.transform.scale(game_over_image, (
            game_over_image.get_width() * (self.screen.get_width() / SCREEN_WIDTH),
            game_over_image.get_height() * (self.screen.get_height() / SCREEN_HEIGHT)))
        self.screen.blit(game_over_image, (0, 0))
        message_to_screen_center(
            self.screen, '탈 락', RED, korean_font, self.screen.get_height() / 2, self.ref_w, self.ref_h)
        pygame.display.update()
        clock.tick(0.5)

    def game_restart(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        pygame.mixer.music.stop()
                        return True
                    elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        pygame.mixer.music.stop()
                        return False
            # 배경 넣기
            self.screen.fill(BLACK)
            # 문구 넣기
            message_to_screen_center(
                self.screen, '재시도 : R', RED, korean_font, self.screen.get_height() * 3 / 8, self.ref_w, self.ref_h)
            message_to_screen_center(
                self.screen, '시작화면으로 이동 : Q', RED, korean_font, self.screen.get_height() / 2, self.ref_w, self.ref_h)
            pygame.display.update()

    def run_game_loop(self, level, score, best_record_mode, select_mode):
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

        # bgm
        try:
            if pygame.mixer.music.get_busy() == False:
                pygame.mixer.music.set_volume(BGM_VOLUME)
                pygame.mixer.music.play(-1)
        except Exception as e:
            print(e)

        while not game_over:
            # 게임 오버 타이머 남은 시간
            left_time = self.game_over_timer.time_checker()

            # 배경 다시 설정
            self.screen.fill(WHITE)
            image_background = pygame.transform.scale(self.background,
                                                      (self.screen.get_width(), self.screen.get_height()))
            self.screen.blit(image_background, (0, 0))

            # 이미지 화면에 맞게 scaling
            pulling_characters = pygame.transform.scale(self.character_pull,
                                                        (self.screen.get_width(), self.screen.get_height()))
            holding_characters = pygame.transform.scale(self.character_hold,
                                                        (self.screen.get_width(), self.screen.get_height()))

            # 버티기 타이머
            elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
            hold_timer = round(float(hold_time - elapsed_time), 1)

            # 현재 레벨, 게임 오버 타이머 화면 좌측 상단에 render
            message_to_screen_left(
                self.screen, 'Level : ' + str(level), WHITE, level_font, self.screen.get_width() / 11,
                             self.screen.get_height() / 30, self.ref_w,
                self.ref_h)
            message_to_screen_left(
                self.screen, "GAME OVER : " + str(left_time), WHITE, level_font, self.screen.get_width() / 4.8,
                             self.screen.get_height() / 14, self.ref_w,
                self.ref_h)
            message_to_screen_left(
                self.screen, "SCORE : " + str(round(score)), WHITE, level_font, self.screen.get_width() / 1.2,
                             self.screen.get_height() / 23, self.ref_w,
                self.ref_h)
            message_to_screen_center(
                self.screen, '승리까지 {} M'.format(int(num_of_press_key_to_clear - num_of_pressed)), WHITE,
                korean_font_small_size,
                self.screen.get_height() / 4,
                self.ref_w, self.ref_h)

            # hold time 렌더링
            if hold_timer > 0:
                self.screen.blit(holding_characters, ((num_of_press_key_to_clear - num_of_pressed), 0))
                message_to_screen_center(
                    self.screen, "Space 누르고 버티기", WHITE, korean_font, self.screen.get_height() * (2 / 3), self.ref_w,
                    self.ref_h)

            # hit time
            if hold_timer <= 0:
                self.screen.blit(pulling_characters, ((num_of_press_key_to_clear - num_of_pressed), 0))
                if hit_time_init:
                    hit_time = RANDOM_NUMBER_FOR_TIMER
                    hit_time_init = False
                hit_time_checker = round(hit_time - (hold_timer) * (-1), 1)
                message_to_screen_center(
                    self.screen, "← → 연타 !", WHITE, korean_large_font, self.screen.get_height() * (2 / 3), self.ref_w,
                    self.ref_h)

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
                    self.screen.get_height() / 2, self.ref_w, self.ref_h)
                pygame.display.update()
                clock.tick(1)
                self.lose_game()
                break
            # 승리조건 만족 -> did_win = True 로 반복문 탈출.
            elif num_of_pressed >= num_of_press_key_to_clear:
                # self.level_clear()
                did_win = True
                break

            # 화면 리사이징
            re_x = self.screen.get_width()
            re_y = self.screen.get_height()
            if (re_x / re_y) != (SCREEN_WIDTH / SCREEN_HEIGHT):
                resize_screen = pygame.display.set_mode((re_x, re_x), pygame.RESIZABLE)
            if re_x > SCREEN_WIDTH or re_y > SCREEN_HEIGHT:
                resize_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

            pygame.display.update()
            clock.tick(FPS_RATE)

        if did_win:
            if best_record_mode:
                message_to_screen_center(self.screen, '축하합니다 통과했습니다! ', WHITE, korean_font,
                                         self.screen.get_height() / 2,
                                         self.ref_w,
                                         self.ref_h)
                pygame.display.update()
                clock.tick(0.5)
                return left_time
            elif select_mode:
                message_to_screen_center(self.screen, '통과!', WHITE, korean_font,
                                         self.screen.get_height() / 3,
                                         self.ref_w,
                                         self.ref_h)
                message_to_screen_center(self.screen, '다음 레벨로 이동합니다. ', WHITE, korean_font,
                                         self.screen.get_height() / 2,
                                         self.ref_w,
                                         self.ref_h)
                pygame.display.update()
                clock.tick(0.5)
                return left_time
            else:
                message_to_screen_center(self.screen, '통과!', WHITE, korean_font,
                                         self.screen.get_height() / 3,
                                         self.ref_w,
                                         self.ref_h)
                message_to_screen_center(self.screen, '다음 게임은 구슬홀짝입니다. ', WHITE, korean_font,
                                         self.screen.get_height() / 2,
                                         self.ref_w,
                                         self.ref_h)
                pygame.display.update()
                clock.tick(0.5)
                return left_time

        # elif self.game_restart():
        #     self.run_game_loop(1)
        else:
            game_over_image = pygame.image.load(get_abs_path(GAME_OVER_LOCATION))
            game_over_image = pygame.transform.scale(game_over_image, (
                game_over_image.get_width() * (self.screen.get_width() / SCREEN_WIDTH),
                game_over_image.get_height() * (self.screen.get_height() / SCREEN_HEIGHT)))
            self.screen.blit(game_over_image, (0, 0))
            message_to_screen_center(
                self.screen, '탈 락', RED, korean_font, self.screen.get_height() / 2, self.ref_w, self.ref_h)
            pygame.display.update()
            clock.tick(0.5)
            pygame.mixer.music.stop()
            return


def start_game(level, score, best_record_mode=False, select_mode=False):
    pygame.init()
    current_screen = pygame.display.get_window_size()
    new_game = TugOfWar(SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT, current_screen)
    score = new_game.start_game(level, score, best_record_mode, select_mode)
    return score

import random

from Games.Dalgona import game_object
from Games.Dalgona.constants import *
from Games.Mugunghwa.game_object import NPC
from Games.game_settings import *

BGM_LOCATION = "Dalgona/Media/bgm.mp3"
PIN_LOCATION = "Dalgona/Media/pin.png"
NPC_RANDRANGE = random.randrange(20, 300)
KIND_OF_NPC = 1
NPC_SPEED = 3
NPC_SIZE_RATIO = 8
GAME_TIME = 50
NUMBER_OF_POINTS = 100
DALGONA_SIZE_RATIO = (3 / 8)
CIRCLE = 1
RECTANGLE = 2
TRIANGLE = 3
STAR = 4
FPS_RATE = 120
SCREEN_STARTING_POINT = (0, 0)
STARTING_LEVEL = 1


class Game:
    NPC_CHANGE_DIRECTION_TIME = 3
    NPC_SIZE = 150

    def __init__(self, width, height, current_screen):
        self.width = width
        self.height = height
        self.half_width = width / 2
        self.half_height = height / 2
        self.center = [self.width / 2, self.height / 2]
        # Screen set-up
        self.game_screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.game_screen.fill(PINK)
        self.shape = random.randrange(CIRCLE, STAR + 1)
        self.rectangle_size = width / RECTANGLE_SHAPE_SIZE_RATIO
        self.half_rectangle = self.rectangle_size / 2
        self.notice_message = True
        pygame.display.set_mode(current_screen, pygame.RESIZABLE)

        # bgm 실행
        try:
            pygame.mixer.music.load(get_abs_path(BGM_LOCATION))
        except Exception as e:
            print(e)

        self.ref_w, self.ref_h = SCREEN_WIDTH,SCREEN_HEIGHT
        self.pin_image = pygame.image.load(get_abs_path(PIN_LOCATION))
        self.npc_size = width / NPC_SIZE_RATIO
        pygame.event.get()

    def start_game(self, level, score, select_mode):
        # walking around NPC
        npc = NPC(self.npc_size, self.npc_size, KIND_OF_NPC)  # 화면을 돌아다닐 npc 생성.

        # bgm
        try:
            if pygame.mixer.music.get_busy() == False:
                pygame.mixer.music.set_volume(BGM_VOLUME)
                pygame.mixer.music.play(-1)
        except Exception as e:
            print(e)

        # 달고나 생성
        dalgona = game_object.Dalgona(self.width, self.height, self.game_screen, NUMBER_OF_POINTS, self.shape)
        game_over_timer = GameOverTimer(GAME_TIME)
        NPC_ticks = pygame.time.get_ticks()

        while True:
            left_time = game_over_timer.time_checker()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    return

            self.game_screen.fill(PINK)

            message_to_screen_left(
                self.game_screen, 'Level:' + str(level), WHITE, level_font, self.game_screen.get_width() / 11,
                                  self.game_screen.get_height() / 30, self.ref_w,
                self.ref_h)
            message_to_screen_left(
                self.game_screen, "GAME OVER : " + str(left_time), WHITE, level_font,
                                  self.game_screen.get_width() / 4.8, self.game_screen.get_height() / 14, self.ref_w,
                self.ref_h)
            message_to_screen_left(
                self.game_screen, "SCORE : " + str(round(score)), BLACK, level_font, self.game_screen.get_width() / 1.2,
                                  self.game_screen.get_height() / 23, self.ref_w,
                self.ref_h)

            pygame.draw.circle(self.game_screen, YELLOW_BROWN,
                               (self.game_screen.get_width() / 2, self.game_screen.get_height() / 2),
                               int(self.width * DALGONA_SIZE_RATIO * self.game_screen.get_width() / SCREEN_WIDTH),
                               int(self.width * DALGONA_SIZE_RATIO * self.game_screen.get_width() / SCREEN_WIDTH))

            # 달고나 모양 그리기.
            if self.shape == CIRCLE:
                pygame.draw.circle(self.game_screen, DARK_BROWN,
                                   (self.game_screen.get_width() / 2, self.game_screen.get_height() / 2),
                                   int(
                                       self.width * CIRCLE_SHAPE_SIZE_RATIO * self.game_screen.get_width() / SCREEN_WIDTH),
                                   int(self.width * SHAPE_WIDTH_RATIO * self.game_screen.get_width() / SCREEN_HEIGHT))
            elif self.shape == RECTANGLE:
                pygame.draw.rect(self.game_screen, DARK_BROWN,
                                 [(self.half_width - self.half_rectangle) * (
                                         self.game_screen.get_width() / SCREEN_WIDTH),
                                  (self.half_height - self.half_rectangle) * (
                                          self.game_screen.get_height() / SCREEN_HEIGHT),
                                  self.rectangle_size * (self.game_screen.get_width() / SCREEN_WIDTH),
                                  self.rectangle_size * (self.game_screen.get_height() / SCREEN_HEIGHT)],
                                 int(self.width * SHAPE_WIDTH_RATIO * self.game_screen.get_width() / SCREEN_WIDTH),
                                 border_radius=RECTANGLE_BORDER_RADIUS)
            elif self.shape == TRIANGLE:
                pygame.draw.polygon(self.game_screen, DARK_BROWN,
                                    [[self.width / 2 * (self.game_screen.get_width() / SCREEN_WIDTH),
                                      self.height / 4 * (self.game_screen.get_height() / SCREEN_HEIGHT)],
                                     [(self.width / 4 + TRIANGLE_ERROR) * (self.game_screen.get_width() / SCREEN_WIDTH),
                                      self.height * (2 / 3) * (self.game_screen.get_height() / SCREEN_HEIGHT)],
                                     [(self.width * (3 / 4) - TRIANGLE_ERROR) * (
                                             self.game_screen.get_width() / SCREEN_WIDTH),
                                      self.height * (2 / 3) * (self.game_screen.get_height() / SCREEN_HEIGHT)]],
                                    int(self.width * SHAPE_WIDTH_RATIO * self.game_screen.get_width() / SCREEN_WIDTH))
            elif self.shape == STAR:
                side_length = self.width / 2
                half_side_length = side_length / 2
                ratio = math.sqrt(3)

                center = (self.width / 2, self.height / 2)
                point1 = [center[0] * (self.game_screen.get_width() / SCREEN_WIDTH),
                          (center[1] - (half_side_length * ratio * (2 / 3))) * (
                                  self.game_screen.get_height() / SCREEN_HEIGHT)]
                point2 = [(center[0] - side_length / 2) * (self.game_screen.get_width() / SCREEN_WIDTH),
                          (center[1] + (half_side_length / ratio)) * (self.game_screen.get_height() / SCREEN_HEIGHT)]
                point3 = [(center[0] + side_length / 2) * (self.game_screen.get_width() / SCREEN_WIDTH),
                          (center[1] + (half_side_length / ratio)) * (self.game_screen.get_height() / SCREEN_HEIGHT)]
                reverse_point1 = [center[0] * (self.game_screen.get_width() / SCREEN_WIDTH),
                                  (center[1] + (half_side_length * ratio * (2 / 3))) * (
                                          self.game_screen.get_height() / SCREEN_HEIGHT)]
                reverse_point2 = [(center[0] - side_length / 2) * (self.game_screen.get_width() / SCREEN_WIDTH),
                                  (center[1] - (half_side_length / ratio)) * (
                                          self.game_screen.get_height() / SCREEN_HEIGHT)]
                reverse_point3 = [(center[0] + side_length / 2) * (self.game_screen.get_width() / SCREEN_WIDTH),
                                  (center[1] - (half_side_length / ratio)) * (
                                          self.game_screen.get_height() / SCREEN_HEIGHT)]

                pygame.draw.polygon(self.game_screen, DARK_BROWN,
                                    [point1, point2, point3],
                                    int(self.width * SHAPE_WIDTH_RATIO * self.game_screen.get_width() / SCREEN_WIDTH))
                pygame.draw.polygon(self.game_screen, DARK_BROWN,
                                    [reverse_point1, reverse_point2, reverse_point3],
                                    int(self.width * SHAPE_WIDTH_RATIO * self.game_screen.get_width() / SCREEN_WIDTH))

            dalgona.draw()

            # 바늘 아트워크
            pygame.event.get()
            if pygame.mouse.get_pressed()[0]:
                x_pos = pygame.mouse.get_pos()[0]
                y_pos = pygame.mouse.get_pos()[1]
                self.game_screen.blit(self.pin_image, (x_pos, y_pos - self.pin_image.get_size()[1]))

            # npc 의 랜덤 움직임.
            npc.BASE_SPEED = NPC_SPEED
            npc.move(self.width)
            npc.draw(self.game_screen)
            NPC_elapsed_time = (pygame.time.get_ticks() - NPC_ticks) / 1000
            NPC_timer = round(float(self.NPC_CHANGE_DIRECTION_TIME - NPC_elapsed_time), 1)
            if NPC_timer <= 0:
                npc.change_direction()
                NPC_ticks = pygame.time.get_ticks()
                NPC_elapsed_time = (pygame.time.get_ticks() - NPC_ticks) / 1000

                # NPC 진행 경로 변경하는 타이머를 이용하여, 초기 알림 메세지를 off 하고 wrong point 위치를 변경.
                dalgona.change_wrong_points()
                self.notice_message = False

            elif NPC_timer > 0 and level == STARTING_LEVEL and self.notice_message:
                # 1 레벨, NPC 의 첫 진로변경 전까지 안내 메세지 렌더링.
                message_to_screen_center(self.game_screen, '빨간 점을 피해 달고나를 뽑으세요. ', WHITE, korean_font_small_size,
                                         self.game_screen.get_height() / 2,
                                         self.ref_w,
                                         self.ref_h)

            if dalgona.check_win()["is_success"] is True:
                message_to_screen_center(self.game_screen, '통과!', WHITE, korean_font,
                                         self.game_screen.get_height() / 3,
                                         self.ref_w,
                                         self.ref_h)

                if select_mode:
                    message_to_screen_center(self.game_screen, '다음 레벨로 이동합니다. ', WHITE, korean_font,
                                             self.game_screen.get_height() / 2,
                                             self.ref_w,
                                             self.ref_h)
                else:
                    message_to_screen_center(self.game_screen, '다음 게임은 줄다리기입니다. ', WHITE, korean_font,
                                             self.game_screen.get_height() / 2,
                                             self.ref_w,
                                             self.ref_h)
                # self.harf_width 제거

                pygame.display.update()
                clock.tick(0.5)
                return round(left_time)
            if left_time <= 0 or dalgona.check_win()["wrong_point_clicked"]:
                game_over_image = pygame.image.load(get_abs_path(GAME_OVER_LOCATION))
                game_over_image = pygame.transform.scale(game_over_image, (
                    game_over_image.get_width() * (self.game_screen.get_width() / SCREEN_WIDTH),
                    game_over_image.get_height() * (self.game_screen.get_height() / SCREEN_HEIGHT)))
                self.game_screen.blit(game_over_image, SCREEN_STARTING_POINT)
                message_to_screen_center(self.game_screen, "탈 락", RED, korean_font, self.game_screen.get_height() / 2,
                                         self.ref_w,
                                         self.ref_h)
                pygame.display.update()
                clock.tick(0.5)
                pygame.mixer.music.stop()
                return

            # 화면 리사이징
            re_x = self.game_screen.get_width()
            re_y = self.game_screen.get_height()
            if (re_x / re_y) != (SCREEN_WIDTH / SCREEN_HEIGHT):
                resize_screen = pygame.display.set_mode((re_x, re_x), pygame.RESIZABLE)
            if re_x > SCREEN_WIDTH or re_y > SCREEN_HEIGHT:
                resize_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

            pygame.display.update()
            clock.tick(FPS_RATE)


def start_game(level, score, select_mode):
    pygame.init()
    current_screen = pygame.display.get_window_size()
    new_game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, current_screen)
    return new_game.start_game(level, score, select_mode)

    # pygame.quit()
    # quit()

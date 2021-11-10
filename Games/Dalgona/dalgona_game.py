import random

import game_object
from Games.Mugunghwa.game_object import NPC
from Games.game_settings import *
from constants import *

BGM_LOCATION = "Dalgona/Media/bgm.mp3"
PIN_LOCATION = "Dalgona/Media/pin.png"
NPC_RANDRANGE = random.randrange(20, 300)
KIND_OF_NPC = 1
NPC_SPEED = 10
NPC_SIZE_RATIO = 8
GAME_TIME = 50
NUMBER_OF_POINTS = 100
DALGONA_SIZE_RATIO = (3 / 8)
CIRCLE = 1
RECTANGLE = 2
TRIANGLE = 3
STAR = 4
FPS_RATE = 20


class Game:
    NPC_CHANGE_DIRECTION_TIME = 3
    NPC_SIZE = 150
    BGM_VOLUME = 0.2

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.half_width = width / 2
        self.half_height = height / 2
        self.center = [self.width / 2, self.height / 2]
        # Screen set-up
        self.game_screen = pygame.display.set_mode((width, height))
        self.game_screen.fill(PINK)
        # self.shape = random.randrange(1,4)
        self.shape = RECTANGLE
        self.rectangle_size = width / RECTANGLE_SHAPE_SIZE_RATIO
        self.half_rectangle = self.rectangle_size / 2
        # bgm 실행
        try:
            pygame.mixer.music.load(get_abs_path(BGM_LOCATION))
        except Exception as e:
            print(e)

        self.ref_w, self.ref_h = self.game_screen.get_size()
        print(get_abs_path(PIN_LOCATION))
        self.pin_image = pygame.image.load(get_abs_path(PIN_LOCATION))
        self.npc_size = width / NPC_SIZE_RATIO

    def start_game(self):
        # walking around NPC
        npc = NPC(self.npc_size, self.npc_size, KIND_OF_NPC)  # 화면을 돌아다닐 npc 생성.
        # bgm
        if pygame.mixer.music.get_busy() == False:
            pygame.mixer.music.set_volume(self.BGM_VOLUME)
            pygame.mixer.music.play(-1)
        # 달고나 생성
        dalgona = game_object.Dalgona(self.width, self.height, self.game_screen, NUMBER_OF_POINTS, self.shape)
        game_over_timer = GameOverTimer(GAME_TIME)
        NPC_ticks = pygame.time.get_ticks()

        while True:
            left_time = game_over_timer.time_checker()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            self.game_screen.fill(PINK)

            message_to_screen_left(self.game_screen, 'GAME OVER: ' + str(left_time), WHITE, level_font, self.width / 5,
                                   self.height / 20,
                                   self.ref_w, self.ref_h)

            pygame.draw.circle(self.game_screen, YELLOW_BROWN, self.center,
                               int(self.width * DALGONA_SIZE_RATIO), int(self.width * DALGONA_SIZE_RATIO))

            # 달고나 모양 그리기.
            if self.shape == CIRCLE:
                pygame.draw.circle(self.game_screen, DARK_BROWN, self.center, int(self.width * CIRCLE_SHAPE_SIZE_RATIO),
                                   int(self.width * SHAPE_WIDTH_RATIO))
            elif self.shape == RECTANGLE:
                pygame.draw.rect(self.game_screen, DARK_BROWN,
                                 [self.half_width - self.half_rectangle, self.half_height - self.half_rectangle,
                                  self.rectangle_size,
                                  self.rectangle_size],
                                 int(self.width * SHAPE_WIDTH_RATIO), border_radius=RECTANGLE_BORDER_RADIUS)
            elif self.shape == TRIANGLE:
                pygame.draw.polygon(self.game_screen, DARK_BROWN,
                                    [[self.width / 2, self.height / 4], [self.width / 4, self.height * (2 / 3)],
                                     [self.width * (3 / 4), self.height * (2 / 3)]], 15)
            elif self.shape == STAR:
                side_length = self.width / 2
                half_side_length = side_length / 2
                ratio = math.sqrt(3)

                center = (self.width / 2, self.height / 2)
                point1 = [center[0], center[1] - (half_side_length * ratio * (2 / 3))]
                point2 = [center[0] - side_length / 2, center[1] + (half_side_length / ratio)]
                point3 = [center[0] + side_length / 2, center[1] + (half_side_length / ratio)]
                reverse_point1 = [center[0], center[1] + (half_side_length * ratio * (2 / 3))]
                reverse_point2 = [center[0] - side_length / 2, center[1] - (half_side_length / ratio)]
                reverse_point3 = [center[0] + side_length / 2, center[1] - (half_side_length / ratio)]

                pygame.draw.polygon(self.game_screen, DARK_BROWN,
                                    [point1, point2, point3], 15)
                pygame.draw.polygon(self.game_screen, DARK_BROWN,
                                    [reverse_point1, reverse_point2, reverse_point3], 15)

            dalgona.draw()

            # 바늘 아트워크
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

            if dalgona.check_win()["is_success"] is True:
                self.game_screen.fill(PINK)
                message_to_screen_center(self.game_screen, "승리!", WHITE, korean_font, self.width / 2, self.ref_w,
                                         self.ref_h)
            if left_time <= 0 or dalgona.check_win()["wrong_point_clicked"]:
                self.game_screen.fill(PINK)
                message_to_screen_center(self.game_screen, "패 배", WHITE, korean_font, self.width / 2, self.ref_w,
                                         self.ref_h)
            pygame.display.update()
            clock.tick(FPS_RATE)


pygame.init()
new_game = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
new_game.start_game()

pygame.quit()
quit()

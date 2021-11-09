import math
import random

import game_object
from Games.Mugunghwa.game_object import NPC
from Games.game_settings import *

BGM_LOCATION = "Media/bgm.mp3"
PIN_LOCATION = "Media/pin.png"
NPC_RANDRANGE = random.randrange(20, 300)
KIND_OF_NPC = 1
NPC_SPEED = 10


class Game:
    NPC_CHANGE_DIRECTION_TIME = 3
    NPC_SIZE = 150
    BGM_VOLUME = 0.2

    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Screen set-up
        self.game_screen = pygame.display.set_mode((width, height))
        self.game_screen.fill(PINK)
        # self.shape = random.randrange(1,4)
        self.shape = 4
        # 1 원 2 네모 3 세모 4 별
        # bgm 실행
        try:
            pygame.mixer.music.load(get_abs_path(BGM_LOCATION))
        except Exception as e:
            print(e)

        self.ref_w, self.ref_h = self.game_screen.get_size()
        self.pin_image = pygame.image.load(get_abs_path(PIN_LOCATION))
        self.npc_size = width / 8

    def start_game(self):
        # walking around NPC
        npc = NPC(self.npc_size, self.npc_size, KIND_OF_NPC)  # 화면을 돌아다닐 npc 생성.
        # bgm
        if pygame.mixer.music.get_busy() == False:
            pygame.mixer.music.set_volume(self.BGM_VOLUME)
            pygame.mixer.music.play(-1)
        # 달고나 생성
        dalgona = game_object.Dalgona(self.width, self.height, self.game_screen, 100, self.shape)
        game_over_timer = GameOverTimer(50)
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

            pygame.draw.circle(self.game_screen, YELLOW_BROWN, [self.width / 2, self.height / 2], 300, 300)

            # 달고나 모양.
            if self.shape == 1:
                pygame.draw.circle(self.game_screen, DARK_BROWN, [self.width / 2 + 10, self.height / 2], 220, 15)
            elif self.shape == 2:
                pygame.draw.rect(self.game_screen, DARK_BROWN,
                                 [self.width / 2 - 150 - 30, self.height / 2 - 150 - 30, self.width / 2.2,
                                  self.width / 2.2],
                                 15, border_radius=10)
            elif self.shape == 3:
                pygame.draw.polygon(self.game_screen, DARK_BROWN,
                                    [[self.width / 2, self.height / 4], [self.width / 4, self.height * (2 / 3)],
                                     [self.width * (3 / 4), self.height * (2 / 3)]], 15)
            elif self.shape == 4:
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

            ######################### PIN IMAGE #############################

            if pygame.mouse.get_pressed()[0]:
                x_pos = pygame.mouse.get_pos()[0]
                y_pos = pygame.mouse.get_pos()[1]
                # print(x_pos, y_pos)
                self.game_screen.blit(self.pin_image, (x_pos, y_pos - self.pin_image.get_size()[1]))
            ##################################################################

            # npc 움직임 파트.
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
            clock.tick(20)


pygame.init()
new_game = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
new_game.start_game()

pygame.quit()
quit()

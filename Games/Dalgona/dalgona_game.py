import math

import game_object
from Games.game_settings import *

bgm_location = "Media/bgm.mp3"
pin_location = "Media/pin.png"
npc_randrange = random.randrange(20, 300)


class GameObject:

    def __init__(self, x, y, width, height):
        self.x_pos = x
        self.y_pos = y
        self.width = width
        self.height = height

    def sprite_image(self, image_path):
        object_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(object_image, (self.width, self.height))

    def draw(self, background):
        background.blit(self.image, (self.x_pos, self.y_pos))


class NPCs(GameObject):
    BASE_SPEED = 10

    # True  = right, False = Left

    def __init__(self, x, y, width, height, kind_of_npc=1):
        super().__init__(x, y, width / 2, height)  # 범위 보정
        if kind_of_npc == 1:
            object_image = pygame.image.load('Media/NPC1.png')
        # elif kind_of_npc == 2:
        #     object_image = pygame.image.load('common_images/NPC2.png')
        # else:
        #     object_image = pygame.image.load('common_images/NPC3.png')
        self.go_forward = False
        self.direction = 1
        # 1 right 2 left 3 up 4 down
        self.image = pygame.transform.scale(object_image, (width * (3 / 4), height))

    def draw(self, background):
        if self.go_forward:
            background.blit(self.image, (self.x_pos, self.y_pos))
        else:
            background.blit(pygame.transform.flip(
                self.image, 1, 0), (self.x_pos, self.y_pos))

    def move(self, max_width):
        if self.x_pos <= 0:
            self.direction = 1
        elif self.x_pos >= max_width:
            self.direction = 2
        elif self.y_pos <= 0:
            self.direction = 4
        elif self.y_pos >= max_width:
            self.direction = 3

        if self.direction == 1:
            self.x_pos += self.BASE_SPEED
            self.go_forward = False
        elif self.direction == 2:
            self.x_pos -= self.BASE_SPEED
            self.go_forward = True
        elif self.direction == 3:
            self.y_pos -= self.BASE_SPEED
        else:
            self.y_pos += self.BASE_SPEED

    def change_direction(self):
        self.direction = random.randrange(1, 5)


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
        try:
            pygame.mixer.music.load(bgm_location)
        except Exception as e:
            print(e)
            
        self.ref_w, self.ref_h = self.game_screen.get_size()
        self.pin_image = pygame.image.load(pin_location)
        self.npc = [npc_randrange, self.width * (1 / 5), 150, 150, 1]

    def start_game(self):
        # walking around NPC
        npc = NPCs(*self.npc)
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

            ########################### NPC ##################################
            npc.move(self.width)
            npc.draw(self.game_screen)
            NPC_elapsed_time = (pygame.time.get_ticks() - NPC_ticks) / 1000
            NPC_timer = round(float(self.NPC_CHANGE_DIRECTION_TIME - NPC_elapsed_time), 1)
            if NPC_timer <= 0:
                npc.change_direction()
                NPC_ticks = pygame.time.get_ticks()
                NPC_elapsed_time = (pygame.time.get_ticks() - NPC_ticks) / 1000
            ################################################################

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

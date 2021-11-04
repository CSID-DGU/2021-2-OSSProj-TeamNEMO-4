import math

import game_object
from Games.game_settings import *


class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Screen set-up
        self.game_screen = pygame.display.set_mode((width, height))
        self.game_screen.fill(PINK)
        # self.shape = random.randrange(1,4)
        self.shape = 4
        pygame.mixer.music.load("Media/bgm.mp3")
        self.ref_w, self.ref_h = self.game_screen.get_size()

    def start_game(self):
        # 달고나 생성.
        if pygame.mixer.music.get_busy() == False:
            pygame.mixer.music.play(-1)
        dalgona = game_object.Dalgona(self.width, self.height, self.game_screen, 100, self.shape)
        game_over_timer = GameOverTimer(50)
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
            if dalgona.check_win():
                self.game_screen.fill(PINK)
                message_to_screen_center(self.game_screen, "승리!", WHITE, korean_font, self.width / 2, self.ref_w,
                                         self.ref_h)
            if left_time <= 0:
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

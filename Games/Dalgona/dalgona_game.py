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
        self.shape = 2

    def start_game(self):
        dalgona = game_object.Dalgona(self.width, self.height, self.game_screen, 16, self.shape)
        game_over_timer = GameOverTimer(50)
        while True:
            left_time = game_over_timer.time_checker()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            self.game_screen.fill(PINK)
            message_to_screen_left(self.game_screen, 'GAME OVER: ' + str(left_time), WHITE, level_font, 0, 0)

            pygame.draw.circle(self.game_screen, YELLOW_BROWN, [self.width / 2, self.height / 2], 300, 300)
            if self.shape == 1:
                pygame.draw.circle(self.game_screen, DARK_BROWN, [self.width / 2 + 10, self.height / 2], 220, 15)
            elif self.shape == 2:
                pygame.draw.rect(self.game_screen, DARK_BROWN,
                                 [self.width / 2 - 150 - 30, self.height / 2 - 150 - 30, self.width / 2.2,
                                  self.width / 2.2],
                                 15, border_radius=10)

            dalgona.draw()
            if dalgona.check_win():
                self.game_screen.fill(PINK)
                message_to_screen_center(self.game_screen, "승리!", WHITE, korean_font, self.width / 2)
            if left_time <= 0:
                self.game_screen.fill(PINK)
                message_to_screen_center(self.game_screen, "패 배", WHITE, korean_font, self.width / 2)
            pygame.display.update()
            clock.tick(20)


pygame.init()
new_game = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
new_game.start_game()

pygame.quit()
quit()

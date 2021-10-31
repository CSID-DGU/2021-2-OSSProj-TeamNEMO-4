from Games.game_settings import *

COLUMN_COUNT = 3
ROW_COUNT = 3


class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Screen set-up
        self.game_screen = pygame.display.set_mode((width, height))
        self.game_screen.fill(PINK)

    def start_game(self):
        while True:
            # main_image = pygame.image.load()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                pygame.draw.circle(self.game_screen, WHITE, [self.width / 2, self.height / 2], 300, 2)
                # 점 만들어서 그거 클릭하는 방식으로 해야겠음.
            pygame.display.update()
            clock.tick(TICK_RATE)


pygame.init()
new_game = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
new_game.start_game()

pygame.quit()
quit()

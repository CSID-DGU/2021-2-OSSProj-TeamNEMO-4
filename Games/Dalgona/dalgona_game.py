import game_object
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
        dot = pygame.image.load("Media/dot.png")
        donut = pygame.image.load("Media/donut.png")

        def printing():
            print(123)

        while True:
            # main_image = pygame.image.load()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            pygame.draw.circle(self.game_screen, YELLOWBROWN, [self.width / 2, self.height / 2], 300, 300)
            pygame.draw.circle(self.game_screen, (175, 118, 43), [self.width / 2 + 10, self.height / 2], 220, 15)
            game_object.Point(self.game_screen, 100, 220, 20)
            pygame.display.update()
            clock.tick(TICK_RATE)


pygame.init()
new_game = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
new_game.start_game()

pygame.quit()
quit()

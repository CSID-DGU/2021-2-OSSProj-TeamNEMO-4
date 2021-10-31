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

    def start_game(self):
        points = []
        for i in range(20):
            theta = (2 * math.pi / 20) * i
            pos_x = self.width / 2 + 100 * math.cos(theta)
            pos_y = self.height / 2 + 100 * math.sin(theta)
            points.append(game_object.Point(self.game_screen, pos_x, pos_y, 5))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            pygame.draw.circle(self.game_screen, YELLOWBROWN, [self.width / 2, self.height / 2], 300, 300)
            pygame.draw.circle(self.game_screen, (175, 118, 43), [self.width / 2 + 10, self.height / 2], 220, 15)
            for i in points:
                i.punching()
            pygame.display.update()
            clock.tick(TICK_RATE)


pygame.init()
new_game = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
new_game.start_game()

pygame.quit()
quit()

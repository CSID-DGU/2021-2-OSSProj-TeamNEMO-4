import pygame
import sys
from Games.game_settings import *


class Game:
    def main(self):
        self.game_over_timer = GameOverTimer(10)
        # 변수 선언
        tmr = 0
        time = 30
        level = 0
        idx = 0
        click = 0
        click_n = 15

        pygame.init()
        pygame.display.set_caption(SCREEN_TITLE)
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # 메세지 배치하는 함수
        def message_to_screen_topLeft(surface, msg, color, font):
            textSurf, textRect = text_objects(msg, color, font)
            surface.blit(textSurf, (0, 0))

        def message_to_screen_topCenter(surface, msg, color, font):
            textSurf, textRect = text_objects(msg, color, font)
            surface.blit(textSurf, (200, 0))

        # 게임 시작화면
        def game_start(self):
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_e:
                            game_run(1)
                        elif event.key == pygame.K_q:
                            pygame.quit()
                            sys.exit()
                message_to_screen_center(screen, '줄다리기 게임', BLUE, korean_font, SCREEN_HEIGHT / 4)
                message_to_screen_left(screen, '[조작법]', BLACK, korean_font_small_size, 150, 300)
                message_to_screen_left(screen, 'A 클릭하여 줄 당기기', BLACK, korean_font_small_size, 150, 350)
                message_to_screen_left(screen, 'D 클릭하여 버티기', BLACK, korean_font_small_size, 150, 400)
                message_to_screen_left(screen, 'E 로 시작, Q로 종료', BLACK, korean_font_small_size, 150, 500)
                pygame.display.update()

        #def game_run(self, level):


new_game = Game()
new_game.main()
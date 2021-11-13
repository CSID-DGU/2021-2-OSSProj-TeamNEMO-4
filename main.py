import pygame
from Games.game_settings import *
from Games.Mugunghwa.Mugunghwa_Game import start_game as start_mugunghwa_game
from Games.Dalgona.dalgona_game import start_game as start_dalgona_game
from Games.MarbleGame.marble_game import start_game as start_marble_game

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800


if __name__ == "__main__":
    SCORE = 0

    while True:
        mugunghwa_score = start_mugunghwa_game()
        if mugunghwa_score:
            SCORE += mugunghwa_score
            print(SCORE)
        else:
            print("패배")
            break
        dalgona_score = start_dalgona_game()
        if dalgona_score:
            SCORE += dalgona_score
            print(SCORE)
        else:
            print("패배")
            break
        marble_score = start_marble_game()
        if marble_score:
            SCORE += marble_score
            print(SCORE)
        else:
            print("패배")
            break

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    ref_w, ref_h = screen.get_size()

    while True:
        screen.fill(PINK)
        message_to_screen_center(screen, '게임 종료', WHITE, korean_font,
                                 SCREEN_WIDTH / 3,
                                 ref_w,
                                 ref_h)
        message_to_screen_center(screen, f'점수는 {SCORE} 점입니다. ', WHITE, korean_font,
                                 SCREEN_WIDTH / 2,
                                 ref_w,
                                 ref_h)
        clock.tick(60)
        pygame.display.update()
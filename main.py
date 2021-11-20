import pygame
from Games.game_settings import *
from Games.Mugunghwa.Mugunghwa_Game import start_game as start_mugunghwa_game
from Games.Dalgona.dalgona_game import start_game as start_dalgona_game
from Games.MarbleGame.marble_game import start_game as start_marble_game
from Games.TugOfWar.TugOfWar import start_game as start_tug_game
from Games.game_menu import main_menu

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800


if __name__ == "__main__":
    SCORE = 0
    LEVEL = 1

    selected = main_menu()

    if selected == "infinite_mode":
        while True:
            mugunghwa_score = start_mugunghwa_game(LEVEL, SCORE)
            if mugunghwa_score:
                SCORE += mugunghwa_score
            else:
                break
            dalgona_score = start_dalgona_game(LEVEL, SCORE)
            if dalgona_score:
                SCORE += dalgona_score
            else:
                break
            marble_score = start_marble_game(LEVEL, SCORE)
            if marble_score:
                SCORE += marble_score
            else:
                break
            tug_score = start_tug_game(LEVEL, SCORE)
            if tug_score:
                SCORE += tug_score
            else:
                break

            LEVEL += 1
    elif selected == "the_best_record_mode":
        while True:
            mugunghwa_score = start_mugunghwa_game(LEVEL, SCORE)
            if mugunghwa_score:
                SCORE += mugunghwa_score
            else:
                break
            dalgona_score = start_dalgona_game(LEVEL, SCORE)
            if dalgona_score:
                SCORE += dalgona_score
            else:
                break
            marble_score = start_marble_game(LEVEL, SCORE)
            if marble_score:
                SCORE += marble_score
            else:
                break
            tug_score = start_tug_game(LEVEL, SCORE, best_record_mode=True)
            if tug_score:
                SCORE += tug_score
            else:
                break
            break

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    ref_w, ref_h = screen.get_size()
    RUNNING = True
    while RUNNING:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
        screen.fill(PINK)
        message_to_screen_center(screen, '게임 종료', WHITE, korean_font,
                                 SCREEN_WIDTH / 3,
                                 ref_w,
                                 ref_h)
        message_to_screen_center(screen, f'점수는 {round(SCORE)} 점입니다. ', WHITE, korean_font,
                                 SCREEN_WIDTH / 2,
                                 ref_w,
                                 ref_h)
        pygame.display.update()
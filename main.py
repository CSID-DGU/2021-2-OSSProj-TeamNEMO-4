import pygame
from Games.Mugunghwa.Mugunghwa_Game import start_game as start_mugunghwa_game
from Games.Dalgona.dalgona_game import start_game as start_dalgona_game
from Games.MarbleGame.marble_game import start_game as start_marble_game

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
        start_marble_game()
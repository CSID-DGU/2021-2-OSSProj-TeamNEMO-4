import pygame
from Games.Mugunghwa.Mugunghwa_Game import start_game as start_mugunghwa_game
from Games.Dalgona.dalgona_game import start_game as start_dalgona_game
from Games.MarbleGame.marble_game import start_game as start_marble_game
if __name__ == "__main__":
    start_mugunghwa_game()
    start_dalgona_game()
    start_marble_game()
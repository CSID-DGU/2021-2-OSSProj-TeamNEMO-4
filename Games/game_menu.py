import sys

import Games.game_button as game_button
from Games.MarbleGame.marble_game import *

# from Games.Dalgona.dalgona_game import *  임포트 문제
# from Games.Mugunghwa.Mugunghwa_Game import * 임포트 문제
# from Games.TugOfWar.TOW_By_Class2 import * 상대경로 오류

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption(SCREEN_TITLE)

imgbutton = pygame.image.load(get_abs_path("button.png"))
while True:
    button = game_button.game_button(screen.get_width() / 3, screen.get_height() / 10, imgbutton)
    button2 = game_button.game_button(screen.get_width() / 3, screen.get_height() / 3.1, imgbutton)
    button3 = game_button.game_button(screen.get_width() / 3, screen.get_height() / 1.85, imgbutton)
    button4 = game_button.game_button(screen.get_width() / 3, screen.get_height() / 1.3, imgbutton)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill(PINK)
    if button.draw(screen):
        print('Mugunghwa')
        '''
        pygame.init()
        new_game = Game(BACKGROUND_LOCATION, SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT)
        new_game.start_game()
        '''
    if button2.draw(screen):
        print('Dalgona')
        '''
        new_game = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
        new_game.start_game()
        '''
    if button3.draw(screen):
        print('TugOfWar')
        '''
        new_game = TugOfWar(SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT)
        new_game.start_game()
        '''
    if button4.draw(screen):
        print('Mable')
        pygame.init()
        new_game = MarbleGame(SCREEN_WIDTH, SCREEN_HEIGHT)
        new_game.start_marble_game()
    '''	
    if exit_button.draw(screen):
        print('EXIT')
    '''
    pygame.display.update()
pygame.quit()

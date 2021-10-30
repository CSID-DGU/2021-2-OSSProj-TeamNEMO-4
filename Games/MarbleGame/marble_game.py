from Games import game_settings
import pygame
import sys

def main():
    pygame.init()
    pygame.display.set_caption(game_settings.SCREEN_TITLE)
    screen=pygame.display.set_mode((game_settings.SCREEN_WIDTH,game_settings.SCREEN_HEIGHT))
    clock=pygame.time.Clock()
    font=pygame.font.Font(None,40)

    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        clock.tick(10)

if __name__=='__main__':
    main()
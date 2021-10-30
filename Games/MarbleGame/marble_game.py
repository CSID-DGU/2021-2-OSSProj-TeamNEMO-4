from Games import game_settings
import pygame
import sys

def main():
    pygame.init()
    pygame.display.set_caption(game_settings.SCREEN_TITLE)
    screen=pygame.display.set_mode((game_settings.SCREEN_WIDTH,game_settings.SCREEN_HEIGHT))
    clock=pygame.time.Clock()
    font=game_settings.korean_font
    tmr=0

    while True:
        tmr=tmr+1
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
        txt=font.render("홀짝 게임 "+str(tmr),True,game_settings.WHITE)
        screen.fill(game_settings.BLACK)
        screen.blit(txt,[100,200])
        pygame.display.update()
        clock.tick(10)

if __name__=='__main__':
    main()
from Games import game_settings
import pygame
import sys
import random

imgBG=pygame.image.load("bg/bg.png")

def main():
    tmr = 0
    time=180
    cball=20
    ball = 20
    ballcnt = 0
    idx=10

    pygame.init()
    pygame.display.set_caption(game_settings.SCREEN_TITLE)
    screen=pygame.display.set_mode((game_settings.SCREEN_WIDTH,game_settings.SCREEN_HEIGHT))
    clock=pygame.time.Clock()
    font=game_settings.korean_font

    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()

        time -=0.1
        cballcnt = random.randint(1, cball)
        key=pygame.key.get_pressed()
        minute = int(time / 60)
        second = int(time % 60)

        txt=font.render("홀짝 게임 "+str(minute)+"분"+str(second)+"초",True,game_settings.WHITE)
        if key[pygame.K_UP] and ballcnt<ball:
            ballcnt+=1
        if key[pygame.K_DOWN]and ballcnt>0:
            ballcnt-=1
        if key[pygame.K_LEFT]:
            if cballcnt%2==0:
                ball-=ballcnt
                cball+=ballcnt
            else:
                ball+=ballcnt
                cball-=ballcnt
        if key[pygame.K_RIGHT]:
            if cballcnt%2==1:
                ball-=ballcnt
                cball+=ballcnt
            else:
                ball+=ballcnt
                cball-=ballcnt

        pball = font.render("구슬 배팅 : " + str(ballcnt), True, game_settings.WHITE)
        pball2 = font.render("구슬 개수 : " + str(ball), True, game_settings.WHITE)
        cballtxt=font.render("상대 구슬 개수 : "+str(cball), True, game_settings.WHITE)
        cballtxt2=font.render("상대 배팅 : "+str(cballcnt), True, game_settings.WHITE)
        screen.fill(game_settings.BLACK)
        screen.blit(imgBG, [0, 0])
        screen.blit(cballtxt,[100,100])
        screen.blit(txt,[100,200])
        screen.blit(pball,[100,300])
        screen.blit(pball2,[100,400])
        screen.blit(cballtxt2, [100, 500])

        pygame.display.update()
        clock.tick(10)

if __name__=='__main__':
    main()
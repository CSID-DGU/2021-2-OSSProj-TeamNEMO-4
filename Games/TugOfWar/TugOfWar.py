import pygame
import random

# Screen properties
SCREEN_TITLE = '오징어 게임'
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
PINK = (227, 62, 126)
# Clock of game
clock = pygame.time.Clock()
pygame.font.init()
# Initiate fonts
large_font = pygame.font.SysFont('comicsans', 75)
STOP_font = pygame.font.SysFont('comicsans', 120)
level_font = pygame.font.SysFont('calibri', 30)
korean_font = pygame.font.Font('../../Font/Pretendard-Medium.otf', 60)
korean_font_small_size = pygame.font.Font('../../Font/Pretendard-Light.otf', 30)
level_font.set_bold(True)


def text_objects(text, color, text_font):
    textSurface = text_font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def message_to_screen_center(surface, msg, color, text_font, y):
    textSurf, textRect = text_objects(msg, color, text_font)
    textRect.center = SCREEN_WIDTH / 2, y
    surface.blit(textSurf, textRect)


def message_to_screen_left(surface, msg, color, font, x, y):
    textSurf, textRect = text_objects(msg, color, font)
    surface.blit(textSurf, (x, y))


class Game:
    FPS = 120
    Click_Num = 15 #Level 당 클릭해야하는 횟수 ex) Level 1: 15번, Level 2: 30번 .....
    TIMER_TIME1 = 30 #Level 1의 제한시간
    TIMER_TIME2 = random.randint(3, 7) #당기기 당기지 않기의 시간

    def __init__(self, title, width, height):
        self.title = title
        self.width = width
        self.height = height
        # Screen set-up
        self.game_screen = pygame.display.set_mode((width, height))
        self.game_screen.fill(WHITE)
        pygame.display.set_caption(title)
        self.stop_timer = False

    def start_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        self.run_game_loop(1)
                    elif event.key == pygame.K_q:
                        return
            #배경 설정
            self.game_screen.fill(WHITE)
            #self.game_screen.blit(self.image, (0, 0)) 추후 이미지 구해 추가 예정
            #배경화면에 문구 추가
            message_to_screen_center(
                self.game_screen, '줄다리기 게임', BLUE, korean_font, self.height/4)
            message_to_screen_left(
                self.game_screen, '[조작법]', BLACK, korean_font_small_size, 150, 300)
            message_to_screen_left(
                self.game_screen, 'A 클릭하여 줄 당기기', BLACK, korean_font_small_size, 150, 350)
            message_to_screen_left(
                self.game_screen, 'D 클릭하여 버티기', BLACK, korean_font_small_size, 150, 400)
            message_to_screen_left(
                self.game_screen, 'E 로 시작, Q로 종료', BLACK, korean_font_small_size, 150, 500)
            pygame.display.update()

    def win_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        return False
                    elif event.key == pygame.K_r:
                        return True
            #문구 입력
            self.game_screen.fill(WHITE)
            message_to_screen_left(
                self.game_screen, '통과하셨습니다', BLUE, large_font, 100, 50)
            message_to_screen_left(
                self.game_screen, 'Press R to Play Again', RED, korean_font_small_size, 150, 200)
            message_to_screen_left(
                self.game_screen, 'Press Q to go to main menu', RED, korean_font_small_size, 150, 350)
            pygame.display.update()

    def lose_game(self):
        message_to_screen_center(
            self.game_screen, '탈 락', RED, korean_font, self.width / 2)
        pygame.display.update()
        clock.tick(1)

    def game_restart(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN
                                                 and event.key == pygame.K_q):
                    return False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    return True
            # Display text for losing
            self.game_screen.fill(PINK)
            message_to_screen_center(
                self.game_screen, '재시작 하려면 R ', WHITE, korean_font, 180)
            message_to_screen_center(
                self.game_screen, '메뉴로 돌아가려면 Q', WHITE, korean_font, 280)

    def run_game_loop(self, level):
        game_over = False
        did_win = True
        click_rate = 0

        print('------------------------------')
        print('LEVEL: ', int(level))

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            self.game_screen.fill(WHITE)

            #타이머1 설정 (전체 제한 시간)
            start_ticks1 = pygame.time.get_ticks()
            elapsed_time1 = (pygame.time.get_ticks() - start_ticks1) / 1000
            timer1 = round(float(self.TIMER_TIME1 - elapsed_time1), 1)

            # 타이머2 설정 (줄 당기는 시간 당기면 안 되는 시간 설정)
            start_ticks2 = pygame.time.get_ticks()
            elapsed_time2 = (pygame.time.get_ticks() - start_ticks2) / 1000
            timer2 = round(float(self.TIMER_TIME2 - elapsed_time2), 1)

            message_to_screen_left(
                self.game_screen, 'Level ' + str(level), WHITE, level_font, 0, 0)

            for event in pygame.event.get():
                if timer2 <= 0:
                    self.stop_timer = True
                    time2 = random.randint(3, 7)
                    time_checker2 = round(time2 - (timer2) * (-1), 1)
                    message_to_screen_center(
                        self.game_screen, "S T O P", RED, large_font, self.height / 2)
                    message_to_screen_center(
                        self.game_screen, f'{time_checker2}', RED, large_font, self.height / 3)
                    if time_checker2 <= 0:
                        self.stop_timer = False
                        start_ticks2 = pygame.time.get_ticks()
                        elapsed_time2 = (pygame.time.get_ticks() - start_ticks2) / 1000
                        timer2 = round(float(self.TIMER_TIME2 - elapsed_time2), 1)
                    else:
                        if event.type == 768:
                            did_win = False
                            self.stop_timer = False
                            break
                elif timer2 > 0:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                        click_rate += 1

                    if click_rate == int(level) * self.Click_Num:
                        did_win = True

            if timer1 <= 0:
                did_win = False
                break

        if did_win:
            if level > 3:
                self.win_game()
            else:
                message_to_screen_left(
                    self.game_screen, 'Level ' + str(int(level) + 1), WHITE, level_font, 0, 0)
                self.run_game_loop(level + 1)
        elif self.game_restart():
            self.run_game_loop(1)
        else:
            return


pygame.init()
new_game = Game(SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT)
new_game.start_game()

pygame.quit()
quit()











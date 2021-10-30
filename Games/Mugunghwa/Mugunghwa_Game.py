# Use base code from "https://github.com/AidenBurgess/CrossGame"

import random

import pygame

import game_object

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
    # 클래스변수
    TICK_RATE = 120  # FPS
    MEDIUM_LEVEL = 2
    HARD_LEVEL = 3
    WIN_LEVEL = 4 + 1.5
    TIMER_TIME = 4  # 술래 뒤도는 카운터.

    def __init__(self, image_path, title, width, height):
        self.title = title
        self.width = width
        self.height = height
        # Screen set-up
        self.game_screen = pygame.display.set_mode((width, height))
        self.game_screen.fill(WHITE)
        pygame.display.set_caption(title)
        background_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(background_image, (width, height))
        self.stop_timer = False

    def start_game(self):
        NPC_1 = game_object.NPC(random.randrange(20, 300), self.width * (1 / 5), 100, 100, 1)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        return
                    elif event.key == pygame.K_x:
                        self.run_game_loop(1)
            # Render background
            self.game_screen.fill(WHITE)
            self.game_screen.blit(self.image, (0, 0))
            # Display main menu text
            message_to_screen_center(
                self.game_screen, '무궁화 꽃이 피었습니다', PINK, korean_font, self.height / 4)
            message_to_screen_left(
                self.game_screen, '[ 조작법 ]', BLACK, korean_font_small_size, 150, 300)
            message_to_screen_left(
                self.game_screen, '방향키로 이동 ', BLACK, korean_font_small_size, 150, 350)
            message_to_screen_left(
                self.game_screen, 'Esc 또는 Q - 일시정지', BLACK, korean_font_small_size, 150, 400)
            message_to_screen_left(
                self.game_screen, 'X - 부스트', BLACK, korean_font_small_size, 150, 450)
            message_to_screen_left(
                self.game_screen, 'X 로 시작, Q 로 종료.', BLACK, korean_font_small_size, 150, 500)
            NPC_1.move(self.width)
            NPC_1.draw(self.game_screen)
            pygame.display.update()

    def pause(self):
        # Render background
        image = pygame.Surface([self.width, self.height])
        image.fill(BLACK)
        # image = pygame.Surface([640,480], pygame.SRCALPHA, 32)
        image.set_alpha(100)
        # image = image.convert_alpha()
        self.game_screen.blit(image, (0, 0))
        # Render text
        message_to_screen_center(
            self.game_screen, 'You have paused', RED, large_font, 50)
        message_to_screen_center(
            self.game_screen, 'Press X to continue', WHITE, large_font, 200)
        message_to_screen_center(
            self.game_screen, 'Press Q or esc to return', WHITE, large_font, 330)
        message_to_screen_center(
            self.game_screen, 'to Main Menu', WHITE, large_font, 380)
        # Update screen
        pygame.display.update()
        # Pause options checking
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        return True
                    elif event.key == pygame.K_x:
                        return False

    def win_game(self):
        NPC_1 = game_object.NPC(random.randrange(20, 300), self.width * (1 / 5), 100, 100, 1)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        return False
                    elif event.key == pygame.K_r:
                        return True
            # Render winning text
            self.game_screen.fill(WHITE)
            message_to_screen_left(
                self.game_screen, 'You Won!', BLUE, large_font, 100, 50)
            message_to_screen_left(
                self.game_screen, 'Press R to Play Again', RED, large_font, 150, 200)
            message_to_screen_left(
                self.game_screen, 'Press Q or Esc', RED, large_font, 150, 350)
            message_to_screen_left(
                self.game_screen, 'to go to main menu', RED, large_font, 150, 400)
            # Display the winner slime
            NPC_1.move(self.width)
            NPC_1.draw(self.game_screen)
            pygame.display.update()

    def lose_game(self):
        message_to_screen_center(
            self.game_screen, '탈 락', RED, korean_font, self.width / 2)
        pygame.display.update()
        clock.tick(1)

    def game_restart(self):
        NPC_1 = game_object.NPC(random.randrange(20, 300), self.width * (1 / 5), 100, 100, 1)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN
                                                 and (event.key == pygame.K_q or event.key == pygame.K_ESCAPE)):
                    return False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    return True
            # Display text for losing
            self.game_screen.fill(PINK)
            message_to_screen_center(
                self.game_screen, '재시작 하려면 R ', WHITE, korean_font, 180)
            message_to_screen_center(
                self.game_screen, '메뉴로 돌아가려면 Q', WHITE, korean_font, 280)
            # Have the loser slime dance around lol
            NPC_1.move(self.width)
            NPC_1.draw(self.game_screen)
            pygame.display.update()

    def run_game_loop(self, level):
        game_over = False
        did_win = True
        boost = 1

        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print('LEVEL: ', int((level - 1) * 2 + 1))

        # 플레이어, 진행요원, 목표물 렌더링.
        particle = game_object.AnimatedSprite(500, 500, 50, 50, 'particle/Particle', 10, 6)
        count = 1
        player = game_object.PC(self.width / 2 - 25, self.height * 0.85, 50, 70)
        # 진행요원 -> 사이즈 비율로 다 맞춰야함. 나중에
        NPC_1 = game_object.NPC(random.randrange(20, 300), self.width * (1 / 5), 100, 100, 1)
        NPC_1.BASE_SPEED *= level * 1.8
        NPC_2 = game_object.NPC(random.randrange(20, 700), self.width * (3 / 7), 80, 80, 2)
        NPC_2.BASE_SPEED *= level * 1.5
        NPC_3 = game_object.NPC(random.randrange(20, 700), self.width * (2 / 3), 160, 150)
        NPC_3.BASE_SPEED *= level * 2
        # 술래
        DOLL = game_object.GameObject(self.width / 2 - 45, 10, 130, 130)
        DOLL.sprite_image('NPC/back.png')
        start_ticks = pygame.time.get_ticks()
        while not game_over:
            for event in pygame.event.get():
                # Quit if player tries to exit
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE or event.key == pygame.K_q):
                    if self.pause():
                        return
            # Determine keypresses to determine dirx and diry
            dir_x, dir_y, boost = self.get_PC_dir()
            # Redraw screen
            self.game_screen.fill(WHITE)
            self.game_screen.blit(self.image, (0, 0))
            # 게임 오브젝트 render
            DOLL.draw(self.game_screen)
            NPC_1.move(self.width)
            NPC_1.draw(self.game_screen)
            NPC_2.move(self.width)
            NPC_2.draw(self.game_screen)
            NPC_3.move(self.width)
            NPC_3.draw(self.game_screen)
            player.move(dir_x, dir_y, self.width, self.height, boost)
            player.draw(self.game_screen, dir_x, dir_y)

            # 무궁화 타이머 설정 stop 이 false 일 때만 진행.
            elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
            timer = round(float(self.TIMER_TIME - elapsed_time), 1)

            # Render boost effects
            if boost > 1:
                particle.next_sprite()
                # Offset the particle to be roughly mid-body
                particle.x_pos = player.x_pos + 3
                particle.y_pos = player.y_pos + 30
                particle.draw(self.game_screen)
            # Display level counter in corner
            message_to_screen_left(
                self.game_screen, 'Level ' + str(int((level - 1) * 2 + 1)), WHITE, level_font, 0, 0)
            if not self.stop_timer:
                message_to_screen_center(
                    self.game_screen, f'Timer: {timer}', BLACK, level_font, self.width * (1 / 2))

            # Detect collision
            try:
                collision = self.detect_all_collisions(
                    level, player, NPC_1, NPC_2, NPC_3, DOLL)
            except:
                try:
                    collision = self.detect_all_collisions(
                        level, player, NPC_1, NPC_2, 0, DOLL)
                except:
                    collision = self.detect_all_collisions(
                        level, player, NPC_1, 0, 0, DOLL)

            # 무궁화 발동
            if timer <= 0:
                # 3초 타이머 걸고 지나면 해제. & 타이머 리셋.
                DOLL.sprite_image('NPC/front.png')
                self.stop_timer = True
                time = 3
                time_checker = round(time - (timer) * (-1), 1)
                message_to_screen_center(
                    self.game_screen, "S T O P !", RED, large_font, self.height / 2)
                message_to_screen_center(
                    self.game_screen, f'{time_checker}', RED, large_font, self.height / 3)
                if time_checker <= 0:
                    DOLL.sprite_image('NPC/back.png')
                    self.stop_timer = False
                    start_ticks = pygame.time.get_ticks()
                    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
                    timer = round(float(self.TIMER_TIME - elapsed_time), 2)
                else:
                    if event.type == 768:  # keydown 감지되면 끝.
                        did_win = False
                        self.stop_timer = False  # 재시작을 위한 stop_timer 원상복귀.
                        DOLL.sprite_image('NPC/back.png')
                        break

            if collision == 'dead':
                did_win = False
                break
            elif collision == 'DOLL':
                # 목표물 도달시 did_win = True 상태로 while 문 탈출.
                break
            pygame.display.update()
            clock.tick(self.TICK_RATE)
        # did_win 이용해 승패 판단 후 다음 프로세스 진행.
        if did_win:
            if level >= self.WIN_LEVEL:
                self.win_game()  # 전체 게임 클리어.
            else:
                message_to_screen_left(
                    self.game_screen, 'Level ' + str(int((level - 1) * 2 + 1)), WHITE, level_font, 0, 0)
                self.run_game_loop(level + 0.5)
        elif self.game_restart():
            self.run_game_loop(1)
        else:
            return

    def get_PC_dir(self, dir_x=0, dir_y=0, boost=1):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            dir_y = 1
        if keys[pygame.K_DOWN]:
            dir_y = -1
        if keys[pygame.K_LEFT]:
            dir_x = -1
        if keys[pygame.K_RIGHT]:
            dir_x = 1
        if keys[pygame.K_x]:
            boost = 2
        return (dir_x, dir_y, boost)

    def detect_all_collisions(self, level, player, NPC_1, NPC_2, NPC_3, DOLL):
        dead = 0
        # if level > self.HARD_LEVEL:
        dead += player.detect_collision(NPC_3)
        # if level > self.MEDIUM_LEVEL:
        dead += player.detect_collision(NPC_2)
        dead += player.detect_collision(NPC_1)
        if dead:
            self.lose_game()
            return 'dead'

        if player.detect_collision(DOLL):
            message_to_screen_center(self.game_screen, 'Next Up, Level ' + str(
                int(level * 2)), WHITE, STOP_font, self.height / 2)
            pygame.display.update()
            clock.tick(1)
            return 'DOLL'


# Start the game up
pygame.init()
new_game = Game('NPC/background.png', SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT)
new_game.start_game()

# After game is finished quit the program
pygame.quit()
quit()

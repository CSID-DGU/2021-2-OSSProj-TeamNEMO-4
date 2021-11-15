# Use base code from "https://github.com/AidenBurgess/CrossGame"

from Games.Mugunghwa import game_object
from Games.game_settings import *


def level_printer(level):
    return 'Level ' + str(int((level - 1) * 2 + 1))


AIM_LOCATION = 'Mugunghwa/NPC/aim.png'
BGM_LOCATION = 'Mugunghwa/Sound/mugunghwa.mp3'
BACKGROUND_LOCATION = 'Mugunghwa/NPC/background.png'
DOLL_BACK_LOCATION = 'Mugunghwa/NPC/back.png'
DOLL_FRONT_LOCATION = 'Mugunghwa/NPC/front.png'
SCREEN_STARTING_POINT = (0, 0)  # 화면 좌측 최상단 point.
STARTING_MESSAGE_Y_POS = (300, 400, 450)  # 시작화면 메세지 출력 y 좌표 => 추후 상대적 값으로 변경 필요.
NPC_1_CODE = 1
NPC_2_CODE = 2
NPC_3_CODE = 3
DEAD_MESSAGE = 'dead'
DOLL_MESSAGE = 'DOLL'
STARTING_LEVEL = 1
KEY_INPUT = 768


class Game:
    TICK_RATE = 120  # FPS
    TIMER_TIME = 5  # 술래 뒤도는 카운터.
    NPC_CHANGE_DIRECTION_TIME = 2
    AIM_CHANGE_DIRECTION_TIME = 1.5
    GAME_OVER_TIMER = 30
    NPC_1_SPEED = 1.8
    NPC_2_SPEED = 2
    NPC_3_SPEED = 1.5
    AIM_SIZE = (500, 350)  # 조준경의 가로 세로 사이즈 => 상대적 값으로 변경 필요.
    AIM_SPEED = 2
    TIMER_UNIT = 1000
    LEVEL_UP_STEP = 0.5

    def __init__(self, image_path, title, width, height):
        self.title = title
        self.width = width
        self.height = height
        self.half_width = width / 2
        self.one_third_screen = (width / 3, height / 3)
        self.game_screen = pygame.display.set_mode((width, height))  # 게임 스크린.
        self.game_screen.fill(WHITE)
        pygame.display.set_caption(title)  # 창 제목을 설정한다.
        background_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(background_image, (width, height))
        self.mugunghwa_timer = False  # 술래가 뒤도는 타이머.
        self.game_over_timer = None  # 전체 타이머
        self.aim_image = pygame.image.load(get_abs_path(AIM_LOCATION))  # 조준경 이미지 로드
        self.ref_w, self.ref_h = self.game_screen.get_size()  # 리사이징을 위한 화면 크기

        # npc 정보.
        self.npc_1_size = width / 8  # 각 npc 들의 화면 크기에 대한 상대적 size.
        self.npc_2_size = width / 10
        self.npc_3_size = width / 5
        # 술래
        self.doll = [self.width * 0.456, self.height / 80, self.width / 8, self.height * 0.1875]
        # 화면 크기에 대한 술래의 비율

        # 플레이어 사이즈. 창 크기에 대한 비율로 나타낸다.
        self.player_character_size = (width / 16, width / 11)
        self.restart_message_y_pos = (180, 280)

        try:
            pygame.mixer.music.load(get_abs_path(BGM_LOCATION))
        except Exception as e:
            print(e)
            print("사운드 로드 오류")

    # npc 생성을 위한 메소드.
    def create_npc(self, kind_of_npc):

        if kind_of_npc == NPC_1_CODE:
            size = self.npc_1_size
        elif kind_of_npc == NPC_2_CODE:
            size = self.npc_2_size
        elif kind_of_npc == NPC_3_CODE:
            size = self.npc_3_size
        return game_object.NPC(size, size, kind_of_npc)

    def start_game(self, level, score):
        npc = self.create_npc(NPC_1_CODE)
        score = self.run_game_loop(level, score)
        return score
        # while True:
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             return
        #         elif event.type == pygame.KEYDOWN:
        #             if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
        #                 return
        #             elif event.key == pygame.K_x:
        #                 score = self.run_game_loop(level, score)
        #                 return score
        # Render background
        # self.game_screen.fill(WHITE)
        # self.game_screen.blit(self.image, SCREEN_STARTING_POINT)
        #
        # # Display main menu text
        # message_to_screen_center(
        #     self.game_screen, '무궁화 꽃이 피었습니다', PINK, korean_font, self.height / 4, self.ref_w, self.ref_h)
        # message_to_screen_center(
        #     self.game_screen, '[ 조작법 ]', BLACK, korean_font_small_size, STARTING_MESSAGE_Y_POS[0], self.ref_w,
        #     self.ref_h)
        # message_to_screen_center(
        #     self.game_screen, '방향키로 이동 ', BLACK, korean_font_small_size, STARTING_MESSAGE_Y_POS[1], self.ref_w,
        #     self.ref_h)
        # message_to_screen_center(
        #     self.game_screen, 'X 로 시작', BLACK, korean_font_small_size, STARTING_MESSAGE_Y_POS[2],
        #     self.ref_w, self.ref_h)
        # npc.move(self.width)
        # npc.draw(self.game_screen)
        # pygame.display.update()

    def lose_game(self):
        game_over_image = pygame.image.load(get_abs_path(GAME_OVER_LOCATION))
        game_over_image = pygame.transform.scale(game_over_image, (self.width, self.height))
        self.game_screen.blit(game_over_image, SCREEN_STARTING_POINT)
        message_to_screen_center(
            self.game_screen, '탈 락', RED, korean_font, self.half_width, self.ref_w, self.ref_h)
        pygame.display.update()
        clock.tick(0.5)

    # def game_restart(self):
    #     npc = self.create_npc(NPC_1_CODE)
    #     while True:
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN
    #                                              and (event.key == pygame.K_q or event.key == pygame.K_ESCAPE)):
    #                 return False
    #             elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
    #                 return True
    #         # Display text for losing
    #         self.game_screen.fill(PINK)
    #         message_to_screen_center(
    #             self.game_screen, '재시작 하려면 R ', WHITE, korean_font, self.restart_message_y_pos[0], self.ref_w,
    #             self.ref_h)
    #         message_to_screen_center(
    #             self.game_screen, '메뉴로 돌아가려면 Q', WHITE, korean_font, self.restart_message_y_pos[1], self.ref_w,
    #             self.ref_h)
    #         # Have the loser slime dance around lol
    #         npc.move(self.width)
    #         npc.draw(self.game_screen)
    #         pygame.display.update()

    def run_game_loop(self, level, score):
        game_over = False
        did_win = True
        # 무궁화 SOUND EFFECTS
        pygame.mixer.music.play(-1)

        # 전체 타이머 설정.
        self.game_over_timer = GameOverTimer(self.GAME_OVER_TIMER)

        # 플레이어, 진행요원, 목표물 렌더링.
        player = game_object.PC(self.half_width, self.height, *self.player_character_size)
        # 진행요원 -> 사이즈 비율로 다 맞춰야함. 나중에
        npc_1 = self.create_npc(NPC_1_CODE)
        npc_2 = self.create_npc(NPC_2_CODE)
        npc_3 = self.create_npc(NPC_3_CODE)
        npc_1.BASE_SPEED = (level * 3) + self.NPC_1_SPEED
        npc_2.BASE_SPEED = (level * 3) + self.NPC_2_SPEED
        npc_3.BASE_SPEED = (level * 3) + self.NPC_3_SPEED
        npcs = [npc_1, npc_2, npc_3]

        # AIM
        aim = game_object.Aim(*self.AIM_SIZE)
        aim.BASE_SPEED *= self.AIM_SPEED

        # 술래
        DOLL = game_object.GameObject(*self.doll)
        DOLL.sprite_image(get_abs_path(DOLL_BACK_LOCATION))

        # 술래 타이머, 진행요원 타이머, 조준경 타이머를 위한 현재 시간 얻어오기.
        start_ticks = pygame.time.get_ticks()
        npc_ticks = pygame.time.get_ticks()
        aim_ticks = pygame.time.get_ticks()

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            # 전체 타이머
            left_time = self.game_over_timer.time_checker()
            if left_time < 0:
                self.lose_game()
                return
            # 캐릭터 방향전환.
            dir_x, dir_y = self.get_PC_dir()
            # Redraw screen
            self.game_screen.fill(WHITE)
            self.game_screen.blit(self.image, SCREEN_STARTING_POINT)
            # 술래 render
            DOLL.draw(self.game_screen)

            # npc 1,2,3 이 담긴 리스트 npcs 의 원소들을 move 후 draw 를 반복.
            for npc in npcs:
                npc.move(self.width)
                npc.draw(self.game_screen)
            player.move(dir_x, dir_y, self.width, self.height)
            player.draw(self.game_screen, dir_x, dir_y)

            # NPC turning timer 설정.
            npc_elapsed_time = (pygame.time.get_ticks() - npc_ticks) / self.TIMER_UNIT
            npc_timer = round(float(self.NPC_CHANGE_DIRECTION_TIME - npc_elapsed_time), 1)
            if npc_timer <= 0:  # npc_timer 가 0 이 되면 모든 NPC 의 진행방향을 변경한다.
                for npc in npcs:
                    npc.change_direction()
                npc_ticks = pygame.time.get_ticks()
                npc_elapsed_time = (pygame.time.get_ticks() - npc_ticks) / self.TIMER_UNIT

            # 무궁화 타이머 설정 stop 이 false 일 때만 진행.
            elapsed_time = (pygame.time.get_ticks() - start_ticks) / self.TIMER_UNIT
            timer = round(float(self.TIMER_TIME - elapsed_time), 1)

            # 현재 레벨, 게임 오버 타이머 화면 좌측 상단에 render
            message_to_screen_left(
                self.game_screen, 'Level:' + str(level), WHITE, level_font, 70, 30, self.ref_w,
                self.ref_h)
            message_to_screen_left(
                self.game_screen, "GAME OVER : " + str(left_time), WHITE, level_font, 165, 65, self.ref_w, self.ref_h)
            message_to_screen_left(
                self.game_screen, "SCORE : " + str(score), BLACK, level_font, self.width - 130, 40, self.ref_w,
                self.ref_h)

            try:
                collision = self.detect_all_collisions(
                    player, npc_1, npc_2, npc_3, DOLL)
            except:
                try:
                    collision = self.detect_all_collisions(
                        player, npc_1, npc_2, 0, DOLL)
                except:
                    collision = self.detect_all_collisions(
                        player, npc_1, 0, 0, DOLL)

            # 무궁화 SOUND EFFECTS
            # 게임 내내 반복된다.
            if pygame.mixer.music.get_busy() is False:
                pygame.mixer.music.play(-1)

            # 무궁화 발동
            if timer <= 0:
                # 3초 타이머 걸고 지나면 해제. & 타이머 리셋.
                DOLL.sprite_image(get_abs_path(DOLL_FRONT_LOCATION))
                self.mugunghwa_timer = True
                time = self.TIMER_TIME
                time_checker = round(time - (timer) * (-1), 1)
                if time_checker <= 0:
                    DOLL.sprite_image(get_abs_path((DOLL_BACK_LOCATION)))
                    self.mugunghwa_timer = False
                    start_ticks = pygame.time.get_ticks()
                    elapsed_time = (pygame.time.get_ticks() - start_ticks) / self.TIMER_UNIT
                    timer = round(float(self.TIMER_TIME - elapsed_time), 2)
                else:
                    # 술래가 뒤돌았을 때 조준경이 돌아다니는 effect
                    aim.move(self.width)
                    aim.draw(self.game_screen)
                    aim_elapsed_time = (pygame.time.get_ticks() - aim_ticks) / self.TIMER_UNIT
                    aim_timer = round(float(self.AIM_CHANGE_DIRECTION_TIME - aim_elapsed_time), 1)
                    if aim_timer <= 0:
                        aim.change_direction()
                        aim_ticks = pygame.time.get_ticks()
                        aim_elapsed_time = (pygame.time.get_ticks() - aim_ticks) / self.TIMER_UNIT

                    if event.type == KEY_INPUT:
                        did_win = False
                        self.mugunghwa_timer = False  # 재시작을 위한 mugunghwa_timer 원상복귀.
                        DOLL.sprite_image(get_abs_path(DOLL_BACK_LOCATION))
                        self.lose_game()
                        break

            if collision == DEAD_MESSAGE:
                # npc 와 충돌시, did_win = False 로 while 문 탈출.
                did_win = False
                break
            elif collision == DOLL_MESSAGE:
                # 목표물 도달시 did_win = True 상태로 while 문 탈출.
                break
            pygame.display.update()
            clock.tick(self.TICK_RATE)

        # did_win 이용해 승패 판단 후 다음 프로세스 진행.
        if did_win:
            # message_to_screen_left(
            #     self.game_screen, level_printer(level), WHITE, level_font, 0, 0, self.ref_w,
            #     self.ref_h)
            # self.run_game_loop(level + self.LEVEL_UP_STEP)
            # 다음 게임으로 넘어가기
            return left_time
        # elif self.game_restart():
        #     self.run_game_loop(STARTING_LEVEL)
        else:
            return

    def get_PC_dir(self, dir_x=0, dir_y=0):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            dir_y = 1
        if keys[pygame.K_DOWN]:
            dir_y = -1
        if keys[pygame.K_LEFT]:
            dir_x = -1
        if keys[pygame.K_RIGHT]:
            dir_x = 1
        return dir_x, dir_y

    def detect_all_collisions(self, player, npc_1, npc_2, npc_3, DOLL):
        dead = 0
        dead += player.detect_collision(npc_3)
        dead += player.detect_collision(npc_2)
        dead += player.detect_collision(npc_1)
        # 충돌이 있었을 경우 lose_game 을 호출 후 DEAD_MESSAGE 를 반환하여 게임을 종료.
        if dead:
            self.lose_game()
            return DEAD_MESSAGE

        # 술래와 충돌했을 때 (게임 클리어) -> DOLL_MESSAGE 를 반환해 게임 승리를 상위 함수로 전달.
        if player.detect_collision(DOLL):
            message_to_screen_center(self.game_screen, '통과!', WHITE, korean_font,
                                     self.one_third_screen[0],
                                     self.ref_w,
                                     self.ref_h)
            message_to_screen_center(self.game_screen, '다음 게임은 달고나 게임입니다. ', WHITE, korean_font,
                                     self.half_width,
                                     self.ref_w,
                                     self.ref_h)
            pygame.display.update()
            clock.tick(0.5)
            return DOLL_MESSAGE


# Start the game up
def start_game(level, score):
    pygame.init()
    new_game = Game(get_abs_path(BACKGROUND_LOCATION), SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT)
    return new_game.start_game(level, score)

    # After game is finished quit the program
    # pygame.quit()
    # quit()

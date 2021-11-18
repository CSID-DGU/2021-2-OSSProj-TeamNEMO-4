import sys

from pygame.locals import *

from Games.game_settings import *

# 화면 구성
mainClock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption(SCREEN_TITLE)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

# 버튼 이미지 주소
img_mode_button = pygame.image.load(get_abs_path("menu_imgs/button_mode.png"))
img_rank_button = pygame.image.load(get_abs_path("menu_imgs/button_rank.png"))
img_select_best_button = pygame.image.load(get_abs_path("menu_imgs/button_select_best.png"))
img_select_game_button = pygame.image.load(get_abs_path("menu_imgs/button_select_game.png"))
img_select_infinite_button = pygame.image.load(get_abs_path("menu_imgs/button_select_ifinite.png"))
img_mugungwha_button = pygame.image.load(get_abs_path("menu_imgs/button_mugunghwa.png"))
img_dalgona_button = pygame.image.load(get_abs_path("menu_imgs/button_dalgona.png"))
img_tug_of_war_button = pygame.image.load(get_abs_path("menu_imgs/button_tug_of_war.png"))
img_marble_game_button = pygame.image.load(get_abs_path("menu_imgs/button_marble_game.png"))
img_exit_button = pygame.image.load(get_abs_path("menu_imgs/button_exit.png"))
img_back_button = pygame.image.load(get_abs_path("menu_imgs/button_back.png"))


# 버튼 생성 함수
def button(x, y, image):
    button = image.get_rect()
    button.topleft = (x, y)
    img_button = image
    img_button = pygame.transform.scale(img_button, (image.get_width() * (screen.get_width() / SCREEN_WIDTH),
                                                     image.get_height() * (screen.get_height() / SCREEN_HEIGHT)))
    screen.blit(img_button, (x, y))
    return button


# 메인 화면 함수
def main_menu():
    click = False  # 클릭 판단 변수
    ref_w, ref_h = screen.get_size()
    while True:
        screen.fill(PINK)
        pygame.display.set_caption("오징어 게임 - 메인 화면")

        mx, my = pygame.mouse.get_pos()  # 마우스 좌표 변수

        # 메인 화면 버튼 생성(모드 선택, 랭킹 보기, exit)
        message_to_screen_center(screen, '오징어 게임', WHITE, korean_large_font, screen.get_height() / 5, ref_w,
                                 ref_h)  # 리사이징을 위해 전체 화면 비율로 위치 지정
        button_mode = button(screen.get_width() / 3, screen.get_height() / 2.8, img_mode_button)
        button_rank = button(screen.get_width() / 3, screen.get_height() / 1.8, img_rank_button)
        button_exit = button(screen.get_width() / 3, screen.get_height() / 1.33, img_exit_button)

        if button_mode.collidepoint((mx, my)):
            if click:
                return select_mode_menu()
        if button_rank.collidepoint((mx, my)):
            if click:
                return show_rank_menu()
        if button_exit.collidepoint((mx, my)):
            if click:
                print("종료")
                sys.exit()

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)


def select_mode_menu():
    click = False  # 클릭 판단 변수
    running = True
    print("모드 선택")
    while running:
        screen.fill(PINK)
        pygame.display.set_caption("오징어 게임 - 모드 선택")

        mx, my = pygame.mouse.get_pos()  # 마우스 좌표 변수

        # 모드 선택 화면 버튼 생성(무한 모드, 최고 기록 모드, 게임 선택 모드)
        button_ifinite = button(screen.get_width() / 3, screen.get_height() / 10, img_select_infinite_button)
        button_best = button(screen.get_width() / 3, screen.get_height() / 3.1, img_select_best_button)
        button_select_game = button(screen.get_width() / 3, screen.get_height() / 1.85, img_select_game_button)
        button_back = button(screen.get_width() / 3, screen.get_height() / 1.32, img_back_button)

        if button_ifinite.collidepoint((mx, my)):
            if click:
                return "infinite_mode"
        if button_best.collidepoint((mx, my)):
            if click:
                return "the_best_record_mode"
        if button_select_game.collidepoint((mx, my)):
            if click:
                select_game_menu()
        if button_back.collidepoint((mx, my)):
            if click:
                running = False
                return main_menu()

        click = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)


def show_rank_menu():
    click = False  # 클릭 판단 변수
    running = True
    print("랭킹 보기")
    while running:
        screen.fill(PINK)
        pygame.display.set_caption("오징어 게임 - 랭킹 보기")

        mx, my = pygame.mouse.get_pos()  # 마우스 좌표 변수

        # 랭킹 보기 화면 버튼 생성(무한 모드 랭킹, 최고 기록 모드 랭킹, 게임 선택 모드 랭킹)
        button_ifinite = button(screen.get_width() / 3, screen.get_height() / 10, img_select_infinite_button)
        button_best = button(screen.get_width() / 3, screen.get_height() / 3.1, img_select_best_button)
        button_select_game = button(screen.get_width() / 3, screen.get_height() / 1.85, img_select_game_button)
        button_back = button(screen.get_width() / 3, screen.get_height() / 1.32, img_back_button)

        if button_ifinite.collidepoint((mx, my)):
            if click:
                print("무한 모드 랭킹")
        if button_best.collidepoint((mx, my)):
            if click:
                print("최고 기록 모드 랭킹")
        if button_select_game.collidepoint((mx, my)):
            if click:
                select_game_rank_menu()
        if button_back.collidepoint((mx, my)):
            if click:
                running = False
                return main_menu()

        click = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)


def select_game_menu():
    click = False  # 클릭 판단 변수
    running = True
    print("게임 선택 모드")
    while running:
        screen.fill(PINK)
        pygame.display.set_caption("오징어 게임 - 게임 선택 모드")

        mx, my = pygame.mouse.get_pos()  # 마우스 좌표 변수

        # 게임 선택 화면 버튼 생성(각 게임)
        button_mugunghwa = button(screen.get_width() / 20, screen.get_height() / 25, img_mugungwha_button)
        button_dalgona = button(screen.get_width() / 1.9, screen.get_height() / 25, img_dalgona_button)
        button_tug_of_war = button(screen.get_width() / 20, screen.get_height() / 2, img_tug_of_war_button)
        button_marble_game = button(screen.get_width() / 1.9, screen.get_height() / 2, img_marble_game_button)

        if button_mugunghwa.collidepoint((mx, my)):
            if click:
                print("무궁화 게임")
        if button_dalgona.collidepoint((mx, my)):
            if click:
                print("달고나 게임")
        if button_tug_of_war.collidepoint((mx, my)):
            if click:
                print("줄다리기 게임")
        if button_marble_game.collidepoint((mx, my)):
            if click:
                print("구슬 홀짝 게임")

        click = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)


def select_game_rank_menu():
    click = False  # 클릭 판단 변수
    running = True
    print("게임 선택 모드 랭킹")
    while running:
        screen.fill(PINK)
        pygame.display.set_caption("오징어 게임 - 게임 선택 모드 랭킹")

        mx, my = pygame.mouse.get_pos()  # 마우스 좌표 변수

        # 게임 선택 선택 화면 랭크 버튼 생성(각 게임)
        button_mugunghwa = button(screen.get_width() / 20, screen.get_height() / 25, img_mugungwha_button)
        button_dalgona = button(screen.get_width() / 1.9, screen.get_height() / 25, img_dalgona_button)
        button_tug_of_war = button(screen.get_width() / 20, screen.get_height() / 2, img_tug_of_war_button)
        button_marble_game = button(screen.get_width() / 1.9, screen.get_height() / 2, img_marble_game_button)

        if button_mugunghwa.collidepoint((mx, my)):
            if click:
                print("무궁화 게임 랭킹")
        if button_dalgona.collidepoint((mx, my)):
            if click:
                print("달고나 게임 랭킹")
        if button_tug_of_war.collidepoint((mx, my)):
            if click:
                print("줄다리기 게임 랭킹")
        if button_marble_game.collidepoint((mx, my)):
            if click:
                print("구슬 홀짝 게임 랭킹")

        click = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)

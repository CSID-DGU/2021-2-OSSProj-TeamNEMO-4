import sys

from pygame.locals import *

from db import *

# 화면 구성
mainClock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption(SCREEN_TITLE)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
ref_w, ref_h = screen.get_size()
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

MENU_TICK_RATE = 60  # 메뉴 화면 초당 프레임.


# fade-in fade-out fade-out
def fade_out(fade):
    fade.fill(PINK)
    for alpha in range(0, MENU_TICK_RATE):
        fade.set_alpha(alpha)
        screen.blit(fade, (0, 0))
        pygame.display.update()


def fade_in(fade, draw_function):
    fade.fill(PINK)
    screen.blit(fade, (0, 0))
    pygame.display.update()
    for alpha in range(0, MENU_TICK_RATE):
        draw_function()
        fade.set_alpha(255 - alpha * 4)
        screen.blit(fade, (0, 0))
        pygame.display.update()


# 버튼 생성 함수
def button(x, y, image):
    button = image.get_rect()
    button.topleft = (x, y)
    img_button = image
    img_button = pygame.transform.scale(img_button, (image.get_width() * (screen.get_width() / SCREEN_WIDTH),
                                                     image.get_height() * (screen.get_height() / SCREEN_HEIGHT)))
    screen.blit(img_button, (x, y))
    return button


# 유저명 받기

def draw_input_box():
    input_box = pygame.Rect(screen.get_width() / 7, screen.get_height() * (3 / 4), screen.get_width() * 0.7,
                            screen.get_height() / 8)
    text = ''
    while True:
        screen.fill(PINK)
        message_to_screen_center(screen, '기록 갱신! 축하합니다!', WHITE, korean_font,
                                 SCREEN_WIDTH / 3,
                                 ref_w,
                                 ref_h)
        message_to_screen_center(screen, f'명예의 전당에 이름을 등록하세요. ', WHITE, korean_font_small_size,
                                 SCREEN_WIDTH / 2,
                                 ref_w,
                                 ref_h)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return text
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
        txt = korean_large_font.render(text, True, BLACK)
        screen.blit(txt, (input_box.x + 10, input_box.y))
        pygame.draw.rect(screen, GRAY, input_box, 5)
        pygame.display.update()
        mainClock.tick(MENU_TICK_RATE)


# 메인 화면 함수

def draw_main_menu():
    screen.fill(PINK)
    pygame.display.set_caption("오징어 게임 - 메인 화면")
    # 메인 화면 버튼 생성(모드 선택, 랭킹 보기, exit)
    message_to_screen_center(screen, '오징어 게임', WHITE, korean_large_font, screen.get_height() / 5, ref_w,
                             ref_h)  # 리사이징을 위해 전체 화면 비율로 위치 지정
    return (
        # mode button
        button(screen.get_width() / 3, screen.get_height() / 2.8, img_mode_button),
        # rank button
        button(screen.get_width() / 3,
               screen.get_height() / 1.8,
               img_rank_button),
        # exit button
        button(
            screen.get_width() / 3, screen.get_height() / 1.33, img_exit_button))


def main_menu():
    click = False  # 클릭 판단 변수
    ref_w, ref_h = screen.get_size()
    fade = pygame.Surface((screen.get_width(), screen.get_height()))
    fade_in(fade, draw_main_menu)
    while True:
        screen.fill(PINK)
        pygame.display.set_caption("오징어 게임 - 메인 화면")

        mx, my = pygame.mouse.get_pos()  # 마우스 좌표 변수
        # 메인 화면 버튼 생성(모드 선택, 랭킹 보기, exit)
        message_to_screen_center(screen, '오징어 게임', WHITE, korean_large_font, screen.get_height() / 5, ref_w,
                                 ref_h)  # 리사이징을 위해 전체 화면 비율로 위치 지정

        button_mode, button_rank, button_exit = draw_main_menu()

        if button_mode.collidepoint((mx, my)):
            if click:
                fade_out(fade)
                return select_mode_menu()
        if button_rank.collidepoint((mx, my)):
            if click:
                fade_out(fade)
                selected = show_rank_menu()
                if selected:
                    render_rank(selected)

        if button_exit.collidepoint((mx, my)):
            if click:
                fade_out(fade)
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
        mainClock.tick(MENU_TICK_RATE)


def draw_select_mode_menu():
    return (
        # infinite_mode button
        button(screen.get_width() / 3, screen.get_height() / 10, img_select_infinite_button),
        # select_mode button
        button(screen.get_width() / 3,
               screen.get_height() / 3.1,
               img_select_best_button),
        # best_record_mode button
        button(
            screen.get_width() / 3, screen.get_height() / 1.85, img_select_game_button),
        # back button
        button(screen.get_width() / 3,
               screen.get_height() / 1.32,
               img_back_button)
    )


def select_mode_menu():
    click = False  # 클릭 판단 변수
    running = True
    fade = pygame.Surface((screen.get_width(), screen.get_height()))
    fade_in(fade, draw_select_mode_menu)

    while running:
        screen.fill(PINK)
        pygame.display.set_caption("오징어 게임 - 모드 선택")
        mx, my = pygame.mouse.get_pos()  # 마우스 좌표 변수
        # 모드 선택 화면 버튼 생성(무한 모드, 최고 기록 모드, 게임 선택 모드)
        button_infinite, button_best, button_select_game, button_back = draw_select_mode_menu()

        if button_infinite.collidepoint((mx, my)):
            if click:
                fade_out(fade)
                return "infinite_mode"
        if button_best.collidepoint((mx, my)):
            if click:
                fade_out(fade)
                return "best_record_mode"
        if button_select_game.collidepoint((mx, my)):
            if click:
                fade_out(fade)
                return select_game_menu()

        if button_back.collidepoint((mx, my)):
            if click:
                fade_out(fade)
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
        mainClock.tick(MENU_TICK_RATE)


def draw_show_rank_menu():
    screen.fill(PINK)
    return (
        # infinite_mode button
        button(screen.get_width() / 3, screen.get_height() / 10, img_select_infinite_button),
        # best_record_mode button
        button(
            screen.get_width() / 3, screen.get_height() / 3.1, img_select_best_button),
        # select_mode button
        button(screen.get_width() / 3,
               screen.get_height() / 1.85,
               img_select_game_button),
        # back button
        button(
            screen.get_width() / 3, screen.get_height() / 1.32, img_back_button)
    )


def render_rank(mode):
    running = True
    if mode == INFINITE or mode == BEST_RECORD:
        score = get_score(mode)
    else:
        score = get_score(SELECT, mode)

    while running:
        screen.fill(PINK)
        # for 문 버그로 직접 작성 - 왜그런지 모르겠
        message_to_screen_center(screen, '명예의 전당', WHITE,
                                 korean_font, screen.get_height() * (1 / 12),
                                 ref_w,
                                 ref_h)
        message_to_screen_center(screen, '뒤로 가려면 esc', BLUE,
                                 korean_font_small_size, screen.get_height() * (11 / 12),
                                 ref_w,
                                 ref_h)
        message_to_screen_center(screen, f'5 위  {score[4]["user"]} : {score[4]["score"]}', WHITE,
                                 korean_font_small_size, screen.get_height() * (5 / 6),
                                 ref_w,
                                 ref_h)
        message_to_screen_center(screen, f'4 위  {score[3]["user"]} : {score[3]["score"]}', WHITE,
                                 korean_font_small_size, screen.get_height() * (4 / 6),
                                 ref_w,
                                 ref_h)
        message_to_screen_center(screen, f'3 위  {score[2]["user"]} : {score[2]["score"]}', WHITE,
                                 korean_font_small_size, screen.get_height() * (3 / 6),
                                 ref_w,
                                 ref_h)
        message_to_screen_center(screen, f'2 위  {score[1]["user"]} : {score[1]["score"]}', WHITE,
                                 korean_font_small_size, screen.get_height() * (2 / 6),
                                 ref_w,
                                 ref_h)
        message_to_screen_center(screen, f'1 위  {score[0]["user"]} : {score[0]["score"]}', WHITE,
                                 korean_font_small_size, screen.get_height() * (1 / 6),
                                 ref_w,
                                 ref_h)
        pygame.display.update()
        mainClock.tick(MENU_TICK_RATE)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False


def show_rank_menu():
    click = False  # 클릭 판단 변수
    running = True
    fade = pygame.Surface((screen.get_width(), screen.get_height()))
    fade_in(fade, draw_show_rank_menu)
    while running:
        screen.fill(PINK)
        pygame.display.set_caption("오징어 게임 - 랭킹 보기")

        mx, my = pygame.mouse.get_pos()  # 마우스 좌표 변수
        # 랭킹 보기 화면 버튼 생성(무한 모드 랭킹, 최고 기록 모드 랭킹, 게임 선택 모드 랭킹)
        button_infinite, button_best, button_select_game, button_back = draw_show_rank_menu()
        if button_infinite.collidepoint((mx, my)):
            if click:
                return INFINITE

        if button_best.collidepoint((mx, my)):
            if click:
                return BEST_RECORD
        if button_select_game.collidepoint((mx, my)):
            if click:
                return select_game_rank_menu()
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
        mainClock.tick(MENU_TICK_RATE)


def draw_select_game_menu():
    screen.fill(PINK)
    return (
        # 무궁화.
        button(screen.get_width() / 8, screen.get_height() / 25, img_mugungwha_button)
        # 달고나.
        , button(screen.get_width() / 1.9, screen.get_height() / 25, img_dalgona_button)
        # 줄다리기.
        , button(screen.get_width() / 8, screen.get_height() / 2.3, img_tug_of_war_button)
        # 구슬홀짝.
        , button(screen.get_width() / 1.9, screen.get_height() / 2.3, img_marble_game_button)
        # 뒤로가기.
        , button(screen.get_width() / 3, screen.get_height() / 1.25, img_back_button)
    )


def select_game_menu():
    click = False  # 클릭 판단 변수
    running = True
    print("게임 선택 모드")
    fade = pygame.Surface((screen.get_width(), screen.get_height()))
    fade_in(fade, draw_select_game_menu)
    while running:
        screen.fill(PINK)
        pygame.display.set_caption("오징어 게임 - 게임 선택 모드")

        mx, my = pygame.mouse.get_pos()  # 마우스 좌표 변수

        # 게임 선택 화면 버튼 생성(각 게임)
        button_mugunghwa, button_dalgona, button_tug_of_war, button_marble_game, button_back = draw_select_game_menu()

        if button_mugunghwa.collidepoint((mx, my)):
            if click:
                return SELECT_MUGUNGHWA
        if button_dalgona.collidepoint((mx, my)):
            if click:
                return SELECT_DALGONA
        if button_tug_of_war.collidepoint((mx, my)):
            if click:
                return SELECT_TUG
        if button_marble_game.collidepoint((mx, my)):
            if click:
                return SELECT_MARBLE
        if button_back.collidepoint((mx, my)):
            if click:
                running = False
                return select_mode_menu()

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
        mainClock.tick(MENU_TICK_RATE)


def draw_select_game_rank_menu():
    screen.fill(PINK)
    return (
        button(screen.get_width() / 8, screen.get_height() / 25, img_mugungwha_button)
        , button(screen.get_width() / 1.9, screen.get_height() / 25, img_dalgona_button)
        , button(screen.get_width() / 8, screen.get_height() / 2.3, img_tug_of_war_button)
        , button(screen.get_width() / 1.9, screen.get_height() / 2.3, img_marble_game_button)
        , button(screen.get_width() / 3, screen.get_height() / 1.25, img_back_button)
    )


def select_game_rank_menu():
    click = False  # 클릭 판단 변수
    running = True
    fade = pygame.Surface((screen.get_width(), screen.get_height()))
    fade_in(fade, draw_select_game_rank_menu)
    while running:
        screen.fill(PINK)
        pygame.display.set_caption("오징어 게임 - 게임 선택 모드 랭킹")

        mx, my = pygame.mouse.get_pos()  # 마우스 좌표 변수

        # 게임 선택 선택 화면 랭크 버튼 생성(각 게임)
        button_mugunghwa, button_dalgona, button_tug_of_war, button_marble_game, button_back = draw_select_game_rank_menu()

        if button_mugunghwa.collidepoint((mx, my)):
            if click:
                return SELECT_MUGUNGHWA
        if button_dalgona.collidepoint((mx, my)):
            if click:
                return SELECT_DALGONA
        if button_tug_of_war.collidepoint((mx, my)):
            if click:
                return SELECT_TUG
        if button_marble_game.collidepoint((mx, my)):
            if click:
                return SELECT_MARBLE
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

        mainClock.tick(MENU_TICK_RATE)

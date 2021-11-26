# Use base code from "https://github.com/AidenBurgess/CrossGame"

import os
import random
from Games.game_settings import *
import pygame

AIM_LOCATION = 'NPC/aim.png'
PC_FRONT_LOCATION = 'PC/LinkFront.png'
PC_BACK_LOCATION = 'PC/LinkBack.png'
PC_LEFT_LOCATION = 'PC/LinkLeft.png'
PC_RIGHT_LOCATION = 'PC/LinkRight.png'
DIRECTION_RANGE = (1, 5)  # [1: 우 2: 좌 3: 상 4: 하] 의 랜덤 범위를 위한 튜플.


def get_abs_path(path):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), path)


class GameObject:

    def __init__(self, x, y, width, height,game_screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.RESIZABLE)):
        self.x_pos = x
        self.y_pos = y
        self.width = width
        self.height = height
        self.game_screen = game_screen
    def sprite_image(self, image_path):
        object_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(object_image, (self.width*(self.game_screen.get_width()/SCREEN_WIDTH), self.height*(self.game_screen.get_height()/SCREEN_HEIGHT)))

    def draw(self, background):
        self.image = pygame.transform.scale(self.image, (self.width * (background.get_width() / SCREEN_WIDTH), self.height * (background.get_height() / SCREEN_HEIGHT)))
        background.blit(self.image, (background.get_width()/2.25, background.get_height()/40))


class NPC(GameObject):
    BASE_SPEED = 3
    # NPC 생성 시 필요한 y 좌표를 위한 값.
    NPC_1_Y_POS = 1 / 5
    NPC_2_Y_POS = 3 / 7
    NPC_3_Y_POS = 2 / 3

    def __init__(self, width, height, kind_of_object=1):
        game_screen_size = pygame.display.get_window_size()
        x_pos = game_screen_size[0] / 2  # npc 생성 x 좌표를 가운데로 설정한다.
        if kind_of_object == 1:
            value = self.NPC_1_Y_POS
        elif kind_of_object == 2:
            value = self.NPC_2_Y_POS
        else:
            value = self.NPC_3_Y_POS
        y_pos = game_screen_size[1] * value  # 각 npc 의 y 좌표를 설정해준다.

        super().__init__(x_pos, y_pos, width, height)  # 게임 난이도 하향을 위한 판정 범위 보정
        self.kind_of_object = kind_of_object
        object_image = pygame.image.load(get_abs_path(f'NPC/NPC{kind_of_object}.png'))
        self.go_forward = False  # go_forward 에 따라 이미지를 좌우로 flip.
        self.direction = 1  # 1 right 2 left 3 up 4 down
        self.image = pygame.transform.scale(object_image, (width * (3 / 4), height))

    def draw(self, background):
        if self.go_forward:
            self.image = pygame.transform.scale(self.image, (
            self.width * (background.get_width() / SCREEN_WIDTH)*(3/4), self.height * (background.get_height() / SCREEN_HEIGHT)))
            background.blit(self.image, (self.x_pos* (background.get_width() / SCREEN_WIDTH), self.y_pos* (background.get_width() / SCREEN_HEIGHT)))
        else:
            self.image = pygame.transform.scale(self.image, (
            self.width * (background.get_width() / SCREEN_WIDTH)*(3/4), self.height * (background.get_height() / SCREEN_HEIGHT)))
            background.blit(pygame.transform.flip(
                self.image, 1, 0),(self.x_pos * (background.get_width() / SCREEN_WIDTH), self.y_pos * (background.get_width() / SCREEN_HEIGHT)))

    def move(self, max_width):
        if self.x_pos <= 0:
            self.direction = 1
        elif self.x_pos >= max_width:
            self.direction = 2
        elif self.y_pos <= 0:
            self.direction = 4
        elif self.y_pos >= max_width:
            self.direction = 3

        if self.direction == 1:
            self.x_pos += self.BASE_SPEED
            self.go_forward = False
        elif self.direction == 2:
            self.x_pos -= self.BASE_SPEED
            self.go_forward = True
        elif self.direction == 3:
            self.y_pos -= self.BASE_SPEED
        else:
            self.y_pos += self.BASE_SPEED

    def change_direction(self):
        self.direction = random.randrange(*DIRECTION_RANGE)


class Aim(NPC):
    BASE_SPEED = 3

    def __init__(self, width, height, game_screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.RESIZABLE)):
        super().__init__(width, height)  # 범위 보정
        object_image = pygame.image.load(get_abs_path(AIM_LOCATION))
        self.image = pygame.transform.scale(object_image, (
            self.width * (game_screen.get_width() / SCREEN_WIDTH), self.height * (game_screen.get_height() / SCREEN_HEIGHT)))


    def move(self, max_width):
        super().move(max_width)
        if self.x_pos <= 0:
            self.direction = 1
        elif self.x_pos >= max_width - self.width: # 조준경이 바뀌지 않는 버그로 수정
            self.direction = 2
        elif self.y_pos <= 0:
            self.direction = 4
        elif self.y_pos >= max_width - self.width:
            self.direction = 3


class PC(GameObject):  # 플레이어 캐릭터
    BASE_SPEED = 4
    object_image = pygame.image.load(get_abs_path(PC_FRONT_LOCATION))
    player_character = pygame.transform.scale(object_image, (50, 70))

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        # Load in all the sprites
        object_image = pygame.image.load(get_abs_path(PC_BACK_LOCATION))
        self.fr_image = pygame.transform.scale(object_image, (width, height))
        object_image = pygame.image.load(get_abs_path(PC_FRONT_LOCATION))
        self.ba_image = pygame.transform.scale(object_image, (width, height))
        object_image = pygame.image.load(get_abs_path(PC_LEFT_LOCATION))
        self.le_image = pygame.transform.scale(object_image, (width, height))
        object_image = pygame.image.load(get_abs_path(PC_RIGHT_LOCATION))
        self.ri_image = pygame.transform.scale(object_image, (width, height))

    # move() 를 통해 바뀐 direction 으로 캐릭터를 계속 그려낸다.
    def draw(self, background, dir_x, dir_y):
        self.player_character=self.ba_image
        self.ba_image = pygame.transform.scale(self.ba_image, (
            self.width * (background.get_width() / SCREEN_WIDTH), self.height * (background.get_height() / SCREEN_HEIGHT)))
        if dir_y > 0:
            self.fr_image = pygame.transform.scale(self.fr_image, (
                self.width * (background.get_width() / SCREEN_WIDTH), self.height * (background.get_height() / SCREEN_HEIGHT)))
            background.blit(self.fr_image, (self.x_pos* (background.get_width() / SCREEN_WIDTH), self.y_pos* (background.get_height() / SCREEN_HEIGHT)))
            self.player_character = self.fr_image
        elif dir_y < 0:
            self.ba_image = pygame.transform.scale(self.ba_image, (
                self.width * (background.get_width() / SCREEN_WIDTH), self.height * (background.get_height() / SCREEN_HEIGHT)))
            background.blit(self.ba_image, (self.x_pos* (background.get_width() / SCREEN_WIDTH), self.y_pos* (background.get_height() / SCREEN_HEIGHT)))
            self.player_character = self.ba_image
        elif dir_x > 0:
            self.ri_image = pygame.transform.scale(self.ri_image, (
                self.width * (background.get_width() / SCREEN_WIDTH), self.height * (background.get_height() / SCREEN_HEIGHT)))
            background.blit(self.ri_image, (self.x_pos* (background.get_width() / SCREEN_WIDTH), self.y_pos* (background.get_height() / SCREEN_HEIGHT)))
            self.player_character = self.ri_image
        elif dir_x < 0:
            self.le_image = pygame.transform.scale(self.le_image, (
                self.width * (background.get_width() / SCREEN_WIDTH), self.height * (background.get_height() / SCREEN_HEIGHT)))
            background.blit(self.le_image, (self.x_pos* (background.get_width() / SCREEN_WIDTH), self.y_pos* (background.get_height() / SCREEN_HEIGHT)))
            self.player_character = self.le_image
        else:
            background.blit(self.player_character, (self.x_pos* (background.get_width() / SCREEN_WIDTH), self.y_pos* (background.get_height() / SCREEN_HEIGHT)))

    # 키 입력에 따른 방향변경
    def move(self, dir_x, dir_y, max_width, max_height):
        MOVE_BY = self.BASE_SPEED
        # 대각선 이동시 1/sqrt(2) 이동
        if dir_x != 0 and dir_y != 0:
            MOVE_BY *= 0.707
        # Define X and Y  movement
        self.y_pos += MOVE_BY * -dir_y
        self.x_pos += MOVE_BY * dir_x
        # Boundary detection
        if self.y_pos > max_height - self.height:
            self.y_pos = max_height - self.height
        elif self.y_pos < 0:
            self.y_pos = 0
        if self.x_pos > max_width - self.width:
            self.x_pos = max_width - self.width
        elif self.x_pos < 0:
            self.x_pos = 0

    def detect_collision(self, other_body):
        if self.y_pos > other_body.y_pos + other_body.height - self.height / 2:
            return False
        elif self.y_pos + self.height < other_body.y_pos:
            return False
        if self.x_pos > other_body.x_pos + other_body.width:
            return False
        elif self.x_pos + self.width < other_body.x_pos:
            return False
        return True
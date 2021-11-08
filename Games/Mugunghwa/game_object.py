# Use base code from "https://github.com/AidenBurgess/CrossGame"

import random

import pygame

AIM_LOCATION = 'NPC/aim.png'


class GameObject:

    def __init__(self, x, y, width, height):
        self.x_pos = x
        self.y_pos = y
        self.width = width
        self.height = height

    def sprite_image(self, image_path):
        object_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(object_image, (self.width, self.height))

    def draw(self, background):
        background.blit(self.image, (self.x_pos, self.y_pos))


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

        super().__init__(x_pos, y_pos, width / 2, height)  # 게임 난이도 하향을 위한 판정 범위 보정
        self.kind_of_object = kind_of_object
        object_image = pygame.image.load(f'NPC/NPC{kind_of_object}.png')
        self.go_forward = False  # go_forward 에 따라 이미지를 좌우로 flip.
        self.direction = 1  # 1 right 2 left 3 up 4 down
        self.image = pygame.transform.scale(object_image, (width * (3 / 4), height))

    def draw(self, background):
        if self.go_forward:
            background.blit(self.image, (self.x_pos, self.y_pos))
        else:
            background.blit(pygame.transform.flip(
                self.image, 1, 0), (self.x_pos, self.y_pos))

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
        self.direction = random.randrange(1, 5)


class Aim(NPC):
    BASE_SPEED = 3

    def __init__(self, width, height):
        super().__init__(width / 2, height)  # 범위 보정
        object_image = pygame.image.load(AIM_LOCATION)
        self.image = pygame.transform.scale(object_image, (width * (3 / 4), height))

    def move(self, max_width):
        super().move(max_width)
        if self.x_pos <= 0:
            self.direction = 1
        elif self.x_pos >= max_width - self.width * 2:
            self.direction = 2
        elif self.y_pos <= 0:
            self.direction = 4
        elif self.y_pos >= max_width - self.width * 2:
            self.direction = 3


class PC(GameObject):  # 플레이어 캐릭터
    BASE_SPEED = 3
    object_image = pygame.image.load('PC/LinkFront.png')
    prev_sprite = pygame.transform.scale(object_image, (50, 70))

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        # Load in all the sprites
        object_image = pygame.image.load('PC/LinkBack.png')
        self.fr_image = pygame.transform.scale(object_image, (width, height))
        object_image = pygame.image.load('PC/LinkFront.png')
        self.ba_image = pygame.transform.scale(object_image, (width, height))
        object_image = pygame.image.load('PC/LinkLeft.png')
        self.le_image = pygame.transform.scale(object_image, (width, height))
        object_image = pygame.image.load('PC/LinkRight.png')
        self.ri_image = pygame.transform.scale(object_image, (width, height))

    # move() 를 통해 바뀐 direction 으로 캐릭터를 계속 그려낸다.
    def draw(self, background, dir_x, dir_y):
        if dir_y > 0:
            background.blit(self.fr_image, (self.x_pos, self.y_pos))
            self.prev_sprite = self.fr_image
        elif dir_y < 0:
            background.blit(self.ba_image, (self.x_pos, self.y_pos))
            self.prev_sprite = self.ba_image
        elif dir_x > 0:
            background.blit(self.ri_image, (self.x_pos, self.y_pos))
            self.prev_sprite = self.ri_image
        elif dir_x < 0:
            background.blit(self.le_image, (self.x_pos, self.y_pos))
            self.prev_sprite = self.le_image
        else:
            background.blit(self.prev_sprite, (self.x_pos, self.y_pos))

    # 키 입력에 따른 방향변경
    def move(self, dir_x, dir_y, max_width, max_height, boost):
        MOVE_BY = self.BASE_SPEED
        # 대각선 이동시 1/sqrt(2) 이동
        if dir_x != 0 and dir_y != 0:
            MOVE_BY *= 0.707
        # 부스트 사용시 속도 증가.
        MOVE_BY *= boost
        # Define X and Y  movement
        self.y_pos += MOVE_BY * -dir_y * (2 / 3)
        self.x_pos += MOVE_BY * dir_x * (2 / 3)
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


class AnimatedSprite(GameObject):

    def __init__(self, x, y, width, height, root_image, num_sprites, speed):
        super().__init__(x, y, width, height)
        self.count = 0
        self.root = root_image
        self.num_sprites = num_sprites
        self.speed = speed
        object_image = pygame.image.load(f'{root_image}' + '1' + '.png')
        self.image = pygame.transform.scale(object_image, (self.width, self.height))

    def next_sprite(self):
        object_image = pygame.image.load(f'{self.root}{self.count // self.speed + 1}.png')
        self.image = pygame.transform.scale(object_image, (self.width, self.height))
        self.x_pos = self.x_pos + 3
        self.y_pos = self.y_pos + 30
        self.count += 1
        if self.count == self.speed * self.num_sprites:
            self.count = 1

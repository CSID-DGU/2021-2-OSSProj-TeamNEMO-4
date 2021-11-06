# Use base code from "https://github.com/AidenBurgess/CrossGame"

import random

import pygame


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

    # True  = right, False = Left

    def __init__(self, x, y, width, height, kind_of_npc=3):
        super().__init__(x, y, width / 2, height)  # 범위 보정
        self.kind_of_npc = kind_of_npc
        if kind_of_npc == 1:
            object_image = pygame.image.load('NPC/NPC1.png')
        elif kind_of_npc == 2:
            object_image = pygame.image.load('NPC/NPC2.png')
        elif kind_of_npc == 3:
            object_image = pygame.image.load('NPC/NPC3.png')
        else:
            object_image = pygame.image.load('NPC/aim.png')
        self.go_forward = False
        self.direction = 1
        # 1 right 2 left 3 up 4 down
        self.image = pygame.transform.scale(object_image, (width * (3 / 4), height))

    def draw(self, background):
        if self.go_forward:
            background.blit(self.image, (self.x_pos, self.y_pos))
        else:
            background.blit(pygame.transform.flip(
                self.image, 1, 0), (self.x_pos, self.y_pos))

    def move(self, max_width):
        if self.kind_of_npc != 4:
            if self.x_pos <= 0:
                self.direction = 1
            elif self.x_pos >= max_width:
                self.direction = 2
            elif self.y_pos <= 0:
                self.direction = 4
            elif self.y_pos >= max_width:
                self.direction = 3
        else:
            if self.x_pos <= 0 - self.width / 2:
                self.direction = 1
            elif self.x_pos >= max_width - self.width / 2:
                self.direction = 2
            elif self.y_pos <= 0 - self.width / 2:
                self.direction = 4
            elif self.y_pos >= max_width - self.width / 2:
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

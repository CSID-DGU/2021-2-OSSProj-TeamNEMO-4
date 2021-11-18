from Games.game_settings import *


class game_button:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.width = image.get_width()
        self.height = image.get_height()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.clicked = False

    def draw(self, surface):
        draw = False
        p = pygame.mouse.get_pos()
        if self.rect.collidepoint(p):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                draw = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        self.image = pygame.transform.scale(self.image, (
            self.width * (surface.get_width() / SCREEN_WIDTH), self.height * (surface.get_height() / SCREEN_HEIGHT)))
        surface.blit(self.image, (self.x, self.y))
        return draw

from Games.game_settings import *


class Button:
    def __init__(self, game_display, x, y, width, height, image, action_image):
        self.game_display = game_display
        self.is_clicked = False
        mouse_x_pos, mouse_y_pos = pygame.mouse.get_pos()

        #마우스 좌표 리사이징
        mouse_x_pos=mouse_x_pos*(SCREEN_WIDTH/self.game_display.get_width())
        mouse_y_pos=mouse_y_pos*(SCREEN_HEIGHT/self.game_display.get_height())
        events = pygame.event.get()
        click = pygame.mouse.get_pressed()

        #버튼 이미지 리사이징
        image=pygame.transform.scale(image, (image.get_width() * (self.game_display.get_width() / SCREEN_WIDTH),
                                                     image.get_height() * (self.game_display.get_height() / SCREEN_HEIGHT)))
        action_image=pygame.transform.scale(action_image, (action_image.get_width() * (self.game_display.get_width() / SCREEN_WIDTH),
                                               action_image.get_height() * (self.game_display.get_height() / SCREEN_HEIGHT)))

        game_display.blit(image, (x*self.game_display.get_width()/SCREEN_WIDTH, y*self.game_display.get_height()/SCREEN_HEIGHT))
        if x + width > mouse_x_pos > x and y + height > mouse_y_pos > y:
            game_display.blit(action_image, (x*self.game_display.get_width()/SCREEN_WIDTH, y*self.game_display.get_height()/SCREEN_HEIGHT))
            if click[0]:
                self.is_clicked = True
        else:
            game_display.blit(image, (x*self.game_display.get_width()/SCREEN_WIDTH, y*self.game_display.get_height()/SCREEN_HEIGHT))


BUTTON_INTERVAL = 25

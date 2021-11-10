import pygame
from Games.game_settings import *

class game_button():
	def __init__(self, x, y, image): #', scale' 지움
		self.width = image.get_width()
		self.height = image.get_height()
		self.image=image
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False
	def draw(self, surface):
		action = False
		pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True
		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False
		self.image = pygame.transform.scale(self.image, (self.width*(surface.get_width()/SCREEN_WIDTH), self.height*(surface.get_height()/SCREEN_HEIGHT)))
		surface.blit(self.image, (self.rect.x, self.rect.y))
		return action
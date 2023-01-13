import pygame
from settings import *

class Ground(pygame.sprite.Sprite): # class Ground
	def __init__(self,groups,scale_factor): # constructor
		super().__init__(groups) # call main class (groups)
		self.sprite_type = 'ground' # create sprite_type with value 'ground'
		
		# load image
		ground_surf = pygame.image.load('graphics/environment/ground.png').convert_alpha()
		self.image = pygame.transform.scale(ground_surf,pygame.math.Vector2(ground_surf.get_size()) * scale_factor)
		
		# set up position
		self.rect = self.image.get_rect(bottomleft = (0,WINDOW_HEIGHT))
		self.pos = pygame.math.Vector2(self.rect.topleft)

		# mask
		self.mask = pygame.mask.from_surface(self.image)

	def update(self,dt): # function update (make the ground move to the left of the screen)
		self.pos.x -= 360 * dt #  decrement pos.x with -360 * dt (movement speed to the left)
		if self.rect.centerx <= 0: # if value of rect.centerx less than 0, then set pos.x into 0
			self.pos.x = 0

		self.rect.x = round(self.pos.x)
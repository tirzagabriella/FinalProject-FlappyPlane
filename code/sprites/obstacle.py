import pygame
from settings import *
from random import choice, randint

class Obstacle(pygame.sprite.Sprite): # class Obstacle
	def __init__(self,groups,scale_factor): # constructor
		super().__init__(groups) # call parent class 'groups'
		self.sprite_type = 'obstacle'

		orientation = choice(('up','down')) # choose random between up or down
		surf = pygame.image.load(f'graphics/obstacles/{choice((0,1))}.png').convert_alpha() # load images
		self.image = pygame.transform.scale(surf,pygame.math.Vector2(surf.get_size()) * scale_factor)
		
		x = WINDOW_WIDTH + randint(40,100)

		if orientation == 'up': # if value of orientation equal up, then set y with WINDOW_HEIGHT + random number between 10-50
			y = WINDOW_HEIGHT + randint(10,50) # to set variable obstacle height
			self.rect = self.image.get_rect(midbottom = (x,y))
		else:
			y = randint(-50,-10) # set y with random number between -50 and -10
			self.image = pygame.transform.flip(self.image,False,True)
			self.rect = self.image.get_rect(midtop = (x,y))

		self.pos = pygame.math.Vector2(self.rect.topleft)

		# mask
		self.mask = pygame.mask.from_surface(self.image)

	def update(self,dt): # function update (make the obstacle move to the left of the screen)
		self.pos.x -= 400 * dt # speed of the movement (obstacle)
		self.rect.x = round(self.pos.x)
		if self.rect.right <= -100:
			self.kill()
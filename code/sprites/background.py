import pygame

class BG(pygame.sprite.Sprite):
	def __init__(self,groups,scale_factor):
		super().__init__(groups)
		bg_image = pygame.image.load('graphics/environment/background.png').convert()

		full_height = bg_image.get_height() * scale_factor
		full_width = bg_image.get_width() * scale_factor
		full_sized_image = pygame.transform.scale (bg_image, (full_width, full_height))
		
		self.image = pygame.Surface((full_width * 2,full_height))
		self.image.blit(full_sized_image,(0,0)) # copies full sized image into left side of self.image surface
		self.image.blit(full_sized_image,(full_width,0)) # copies full sized image into right side of self.image surface

		self.rect = self.image.get_rect(topleft = (0,0))
		self.pos = pygame.math.Vector2(self.rect.topleft) # prepare vector2 to be later used when modifying movement

	def update(self,dt): # function update (make the background move to the left side of the screen)
		self.pos.x -= 300 * dt # decrement pos.x with -300 * dt (delta time)
		if self.rect.centerx <= 0: # if value of rect.centerx less than 0, then set pos.x into 0
			self.pos.x = 0
		self.rect.x = round(self.pos.x)
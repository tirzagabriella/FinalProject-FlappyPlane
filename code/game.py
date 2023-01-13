import pygame, time, sys
from settings import *
from sprites.background import BG
from sprites.ground import Ground
from sprites.obstacle import Obstacle
from sprites.plane import Plane

class Game:
	def __init__(self):
		
		# setup
		pygame.init()
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
		pygame.display.set_caption('Flappy Plane') # game title "Flappy Plane"
		self.clock = pygame.time.Clock()
		self.active = True # create active variable with initial value true

		# sprite groups
		self.all_sprites = pygame.sprite.Group()
		self.collision_sprites = pygame.sprite.Group()

		# scale factor
		bg_height = pygame.image.load('graphics/environment/background.png').get_height() # load background
		self.scale_factor = WINDOW_HEIGHT / bg_height

		# sprite setup 
		BG(self.all_sprites,self.scale_factor) # create Background
		Ground([self.all_sprites,self.collision_sprites],self.scale_factor) # create Ground
		self.plane = Plane(self.all_sprites,self.scale_factor / 1.7) # init Plane

		# timer
		self.obstacle_timer = pygame.USEREVENT # custom event to time when obstacles appear (custom event ids available to be used are 24-32 (1-23 are predefined events). pygame.USEREVENT's value is 24)
		pygame.time.set_timer(self.obstacle_timer,1200) # set up timer, so that obstacles appears every 1.2s

		# text
		self.font = pygame.font.Font('graphics/font/BD_Cartoon_Shout.ttf',30) # load ttf file for font
		self.score = 0 # initiate variable score with value 0
		self.start_offset = 0 # initiate variable start_offset with value 0

		# menu
		self.menu_surf = pygame.image.load('graphics/ui/menu.png').convert_alpha() # load menu image
		self.menu_rect = self.menu_surf.get_rect(center = (WINDOW_WIDTH / 2,WINDOW_HEIGHT / 2)) # set menu position in the center

		# music 
		self.music = pygame.mixer.Sound('sounds/music.wav') # load sound music.wav
		self.music.play(loops = -1)

	def crash(self):
		# when a crash/collision happened between plane and a collision sprite, 
		# or if plane drops down (pos below or equal to 0)
		if pygame.sprite.spritecollide(self.plane,self.collision_sprites,False,pygame.sprite.collide_mask)\
		or self.plane.rect.top <= 0:
			# remove old obstacle sprites
			for sprite in self.collision_sprites.sprites():
				if sprite.sprite_type == 'obstacle': 
					sprite.kill()

			self.active = False # set up active into False
			self.plane.kill()

	def increment_score(self): # function to increment score
		if self.active: # if active equal True, then update score's value
			self.score = (pygame.time.get_ticks() - self.start_offset) // 1200 # increment score every 1.2s
			y = WINDOW_HEIGHT / 10
		else: # either, update y's value
			y = WINDOW_HEIGHT / 2 + (self.menu_rect.height / 1.5)

		score_surf = self.font.render(str(self.score),True,'black') # show score value
		score_rect = score_surf.get_rect(midtop = (WINDOW_WIDTH / 2,y)) # set score value position
		self.display_surface.blit(score_surf,score_rect)

	def run(self):
		last_time = time.time()

		self.active = False
		
		# to keep the game going until terminated
		while True:
			# delta time
			dt = time.time() - last_time
			last_time = time.time()

			# event loop
			# get all events in-game and determine the type of event.
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					if self.active:
						self.plane.jump()
					else:
						self.plane = Plane(self.all_sprites,self.scale_factor / 1.7)
						self.active = True
						self.start_offset = pygame.time.get_ticks()

				if event.type == self.obstacle_timer and self.active: # create obstacle if active and event type is equal to obstacle_timer event
					Obstacle([self.all_sprites,self.collision_sprites],self.scale_factor * 1.1)
			
			# game logic
			self.display_surface.fill('black') # initiate screen with black color
			self.all_sprites.update(dt) # runs all sprite's update function 
			self.all_sprites.draw(self.display_surface)
			self.increment_score() # call function increment_score

			if self.active: 
				self.crash() # func to detect collision
			else:
				self.display_surface.blit(self.menu_surf,self.menu_rect) # show menu when not active/we die

			pygame.display.update()
			# self.clock.tick(FRAMERATE)
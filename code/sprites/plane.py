import pygame
from settings import *

class Plane(pygame.sprite.Sprite): # class Plane
	def __init__(self,groups,scale_factor): #constructor
		super().__init__(groups) # call parent class 'groups'

		# image 
		self.import_frames(scale_factor)
		self.frame_index = 0
		self.image = self.frames[self.frame_index]

		# rect
		self.rect = self.image.get_rect(midleft = (WINDOW_WIDTH / 20,WINDOW_HEIGHT / 2))
		self.pos = pygame.math.Vector2(self.rect.topleft)

		# movement
		self.gravity = 600
		self.direction = 0

		# mask
		self.mask = pygame.mask.from_surface(self.image)

		# sound
		self.jump_sound = pygame.mixer.Sound('sounds/jump.wav')
		self.jump_sound.set_volume(0.3)

	def import_frames(self,scale_factor): # function import_frames
		self.frames = [] # initiate frame with empty list
		for i in range(3): # do looping 3 times to load 3 images
			surf = pygame.image.load(f'graphics/plane/red{i}.png').convert_alpha()
			scaled_surface = pygame.transform.scale(surf,pygame.math.Vector2(surf.get_size())* scale_factor)
			self.frames.append(scaled_surface) # append value of scaled_surface into frames

	def apply_gravity(self,dt): # function apply_gravity
		self.direction += self.gravity * dt # increment value of direction with value of gravity * dt
		self.pos.y += self.direction * dt # increment value of pos.y with value of direction * dt
		self.rect.y = round(self.pos.y)

	def jump(self): # function jump
		self.jump_sound.play() # call function play
		self.direction = -400 # set value of direction into -400 

	def animate(self,dt): # function animate
		self.frame_index += 10 * dt # increment value of frame_index with 10 * dt
		if self.frame_index >= len(self.frames): # if value of frame_index more than equal total of frames, then set frame_index into 0 (repeat plane animation)
			self.frame_index = 0
		self.image = self.frames[int(self.frame_index)]

	def rotate(self): # function rotate
		rotated_plane = pygame.transform.rotozoom(self.image,-self.direction * 0.06,1) # set plane rotation (so that plane's direction is aligned with the parabolic trajectory)
		self.image = rotated_plane
		self.mask = pygame.mask.from_surface(self.image)

	def update(self,dt): # function update
		self.apply_gravity(dt) # call function apply_gravity
		self.animate(dt) # call function animate
		self.rotate() # call function rotate
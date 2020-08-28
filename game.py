from __future__ import print_function
import neat
import time 
import os
import random
import pygame

pygame.font.init()
WIDTH = 500
HEIGHT = 800
pygame.transform
BIRD_IMGS = [ pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
			pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
			pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png')))]

PIPE_IMG =pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
BASE_IMG =pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
BG_IMG =pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
STAT_FONT = pygame.font.SysFont("comicsans", 50)

class Bird:
	IMGS = BIRD_IMGS
	MAX_ROTATAION = 25
	ROT_VEL = 20
	ANIMATION_TIME = 5

	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.tilt = 0
		self.tick_count = 0
		self.vel = 0
		self.height = self.y
		self.img_count = 0
		self.img = self.IMGS[0]

	def jump(self):
		self.vel = -10.5
		self.tick_count = 0
		self.tilt = 30
		self.height = self.y
	#every frame!
	def move(self):
		self.tick_count += 1
		# -x**2 parabole
		displace = self.vel * self.tick_count + 1.5 * self.tick_count ** 2
		if displace >= 16:
			displace = 16
		if displace < 0:
			displace -= 2

		self.y = self.y + displace
		if displace < 0 or self.y < self.height + 50:
			if self.tilt == self.MAX_ROTATAION:
				self.tilt = self.MAX_ROTATAION
		else:
			if self.tilt > -90 :
				self.tilt -= self.ROT_VEL
	
	def draw(self, win):
		self.img_count += 1

		if self.img_count < self.ANIMATION_TIME:
			self.img = self.IMGS[0]
		elif self.img_count < self.ANIMATION_TIME * 2:
			self.img = self.IMGS[1]
		elif self.img_count < self.ANIMATION_TIME * 3:
			self.img = self.IMGS[2]
		elif self.img_count < self.ANIMATION_TIME * 4:
			self.img = self.IMGS[1]
		elif self.img_count < self.ANIMATION_TIME * 4 + 1:
			self.img = self.IMGS[0]
			self.img_count = 0

		if self.tilt <= -80 :
			self.img = self.IMGS[1]
			self.img_count = self.ANIMATION_TIME * 2

		rotated_image = pygame.transform.rotate(self.img, self.tilt)
		new_rect = rotated_image.get_rect(center = self.img.get_rect(topleft = (self.x, self.y)).center)
		win.blit(rotated_image, new_rect.topleft)

	def get_mask(self):
		return pygame.mask.from_surface(self.img)


class Pipe:
	GAP = 200
	VEL = 4

	def __init__(self, x):
		self.x = x
		self.height = 0

		self.top = 0
		self.bottom = 0
		self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
		self.PIPE_BOTTOM = PIPE_IMG

		self.passed = False
		self.set_height()

	def set_height(self):
		self.height = random.randrange(50,450)
		self.top = self.height - self.PIPE_TOP.get_height() 
		self.bottom = self.height + self.GAP

	def move(self):
		self.x -= self.VEL

	def draw(self, win):
		win.blit(self.PIPE_TOP, (self.x, self.top))
		win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))  

	def collide(self, bird):
		bird_mask = bird.get_mask()
		top_mask = pygame.mask.from_surface(self.PIPE_TOP)
		bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
		
		top_offset = (int(self.x - bird.x), int(self.top - round(bird.y)))
		bottom_offset = (int(self.x - bird.x),int( self.bottom - round(bird.y)))
		
		b_point = bird_mask.overlap(bottom_mask, bottom_offset)
		t_point = bird_mask.overlap(top_mask,top_offset)

		if t_point or b_point :
			return True
		return False

class Base:
	VEL = 3
	WIDTH = BASE_IMG.get_width()
	IMG = BASE_IMG

	def __init__(self, y):
		self.y = y
		self.x1 = 0
		self.x2 = self.WIDTH

	def move(self):
		self.x1 -= self.VEL
		self.x2 -= self.VEL

		if self.x1 + self.WIDTH < 0:
			self.x1 = self.x2 + self.WIDTH
		if self.x2 + self.WIDTH < 0:
			self.x2 = self.x1 + self.WIDTH
	def draw(self, win):
		win.blit(self.IMG, (self.x1, self.y))
		win.blit(self.IMG, (self.x2, self.y))		

def drawWindow(win, bird, pipes, base, score):
	win.blit(BG_IMG, (0,0))
	for pipe in pipes:
		pipe.draw(win)

	text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
	win.blit(text, (WIDTH - 10 - text.get_width(),10 ))
	base.draw(win)
	bird.draw(win)
	pygame.display.update()

#gameloop for the game
def GameOver(win, score):
	win.blit(BG_IMG, (0,0))
	text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
	win.blit(text, (int(WIDTH- text.get_width() / 2 ), int(HEIGHT / 2 )))

def main():
	bird = Bird(230, 350)
	base = Base(730)
	pipe_gap = 550
	score = 0
	pipes = [Pipe(pipe_gap)]
	win = pygame.display.set_mode((WIDTH, HEIGHT))
	add_pipe = False
	clock = pygame.time.Clock()
	running = True
	while running :
		clock.tick(30)
		for event in pygame.event.get() :
			if event.type == pygame.QUIT :
				running = False
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE :
				bird.jump()

		rem = []
		base.move()
		bird.move()
		for pipe in pipes:
			if pipe.collide(bird):
				running = False
				GameOver(win, score)
			if bird.y < 0 or bird.y > HEIGHT - 110:
				running = False
				pygame.quit()
				quit()
			if not pipe.passed and pipe.x < bird.x:
				pipe.passed = True
				add_pipe = True
				score += 1
			if pipe.x + pipe.PIPE_BOTTOM.get_width() < 0:
				rem.append(pipe)
			pipe.move()
		if add_pipe:
			add_pipe = False
			pipes.append(Pipe(pipe_gap))
		for r in rem:
			pipes.remove(r)
		drawWindow(win, bird, pipes, base, score )


if __name__ == '__main__':
	main()

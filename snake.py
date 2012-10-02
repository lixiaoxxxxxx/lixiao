import pygame
from pygame.locals import *
from sys import exit
import random

#-------------------------
#vars
sign = 0
sign1 = 0
clock = pygame.time.Clock()
alive = 1
block_size = 5
gap = 1
length = (100 * (block_size + gap) + gap)
blocks = []
pygame.init()
screen = pygame.display.set_mode((length, length), 0, 32)
snake_len = 45
FPS = 55
loc = (0, 0)
flag = 0

#-------------------------
#class

class block:
	x = 0
	y = 0
	rect = (0, 0)
	direction = "none"
	def __init__(self, x, y, direction):
		self.x = x
		self.y = y
		self.direction = direction
		self.rect = ((x * (block_size + gap), y * (block_size + gap)), (block_size, block_size))
	def __del__(self):
		pass


#-------------------------
#funcs  define

def eat():
	global snake_len
	global flag
	tx = blocks[0].x
	ty = blocks[0].y
	if loc == (tx, ty):
		ex = blocks[snake_len - 1].x
		ey = blocks[snake_len - 1].y
		ed = blocks[snake_len - 1].direction
		if ed is 'w':
			blocks.append(block(ex, ey + 1, ed))
			snake_len = snake_len + 1
		elif ed is 's':
			blocks.append(block(ex, ey - 1, ed))
			snake_len = snake_len + 1
		elif ed is 'a':
			blocks.append(block(ex + 1, ey, ed))
			snake_len = snake_len + 1
		elif ed is 'd':
			blocks.append(block(ex - 1, ey, ed))
			snake_len = snake_len + 1
		flag = 0

def spawn():
	global loc
	global flag
	while flag is 0:
		loc = (random.randint(0, 99), random.randint(0, 99))
		for box in blocks:
			if loc == (box.x, box.y):
				continue
			if loc[0] is blocks[0].x or loc[1] is blocks[0].y:
				continue
			else:
				flag = 1
				break
	if flag is 1:
		pygame.draw.rect(screen, (100, 100, 150),((loc[0] * (block_size + gap), loc[1] * (block_size + gap)), (block_size, block_size)), 0)

def avoidself():
	global blocks
	global sign
	tx = blocks[0].x
	ty = blocks[0].y
	td = blocks[0].direction
	if td is 'w':
		for i in range (1, snake_len):
			if ty - 1 is blocks[i].y and tx is blocks[i].x:
				sign = 1
				if blocks[i - 1].x > tx:
					blocks[0].direction = 'a'
				if blocks[i - 1].x < tx:
					blocks[0].direction = 'd'
				if blocks[i - 1].x is tx:
					if blocks[i + 1].x < tx:
						blocks[0].direction = 'a'
					if blocks[i + 1].x > tx:
						blocks[0].direction = 'd'
	if td is 's':
		for i in range (1, snake_len):
			if ty + 1 is blocks[i].y and tx is blocks[i].x:
				sign = 1
				if blocks[i - 1].x > tx:
					blocks[0].direction = 'a'
				if blocks[i - 1].x < tx:
					blocks[0].direction = 'd'
				if blocks[i - 1].x is tx:
					if blocks[i + 1].x < tx:
						blocks[0].direction = 'a'
					if blocks[i + 1].x > tx:
						blocks[0].direction = 'd'
	if td is 'a':
		for i in range (1, snake_len):
			if ty is blocks[i].y and tx - 1 is blocks[i].x:
				sign = 1
				if blocks[i - 1].y > ty:
					blocks[0].direction = 'w'
				if blocks[i - 1].y < ty:
					blocks[0].direction = 's'
				if blocks[i - 1].y is ty:
					if blocks[i + 1].y < ty:
						blocks[0].direction = 'w'
					if blocks[i + 1].y > ty:
						blocks[0].direction = 's'
	if td is 'd':
		for i in range (1, snake_len):
			if ty is blocks[i].y and tx + 1 is blocks[i].x:
				sign = 1
				if blocks[i - 1].y > ty:
					blocks[0].direction = 'w'
				if blocks[i - 1].y < ty:
					blocks[0].direction = 's'
				if blocks[i - 1].y is ty:
					if blocks[i + 1].y < ty:
						blocks[0].direction = 'w'
					if blocks[i + 1].y > ty:
						blocks[0].direction = 's'
def avoidwall():
	global blocks
	global loc
	global sign
	tx = blocks[0].x
	ty = blocks[0].y
	td = blocks[0].direction
	for i in range (1, snake_len):
		if td is 'w' and ty - 1 < 0:
			if tx - 1 is blocks[i].x and ty is blocks[i].y:
				sign1 = 1
				blocks[0].direction = 'd'
			if tx + 1 is blocks[i].x and ty is blocks[i].y:
				sign1 = 1
				blocks[0].direction = 'a'
		if td is 'a' and tx - 1 < 0:
			if tx is blocks[i].x and ty - 1 is blocks[i].y:
				sign1 = 1
				blocks[0].direction = 's'
			if tx is blocks[i].x and ty + 1 is blocks[i].y:
				sign1 = 1
				blocks[0].direction = 'w'
		if td is 's' and ty + 1 >= 100:
			if tx - 1 is blocks[i].x and ty is blocks[i].y:
				sign1 = 1
				blocks[0].direction = 'd'
			if tx + 1 is blocks[i].x and ty is blocks[i].y:
				sign1 = 1
				blocks[0].direction = 'a'
		if td is 'd' and tx + 1 >= 100:
			if tx is blocks[i].x and ty - 1 is blocks[i].y:
				sign1 = 1
				blocks[0].direction = 's'
			if tx is blocks[i].x and ty + 1 is blocks[i].y:
				sign1 = 1
				blocks[0].direction = 'w'
def ai_setdir():
	global blocks
	global loc
	lx = loc[0]
	ly = loc[1]
	tx = blocks[0].x
	ty = blocks[0].y
	td = blocks[0].direction
#---------
	if lx < tx and ly < ty:
		if td is 'd':
			blocks[0].direction = 'w'
		if td is 's':
			blocks[0].direction = 'a'
#---------
	if lx < tx and ly > ty:
		if td is 'd':
			blocks[0].direction = 's'
		if td is 'w':
			blocks[0].direction = 'a'
#---------
	if lx > tx and ly < ty:
		if td is 'a':
			blocks[0].direction = 'w'
		if td is 's':
			blocks[0].direction = 'd'
#---------
	if lx > tx and ly > ty:
		if td is 'w':
			blocks[0].direction = 'd'
		if td is 'a':
			blocks[0].direction = 's'


def ai ():
	global sign
	global sign1
	if sign1 is 1:
		avoidwall()
	else:
		avoidself()
		if sign is 0:
			ai_setdir()
			global blocks
			global loc
			lx = loc[0]
			ly = loc[1]
			tx = blocks[0].x
			ty = blocks[0].y
			td = blocks[0].direction
			if tx is lx:
				if ly < ty:
					blocks[0].direction = 'w'
				if ly > ty:
					blocks[0].direction = 's'
			if ty is ly:
				if lx < tx:
					blocks[0].direction = 'a'
				if lx > tx:
					blocks[0].direction = 'd'
			avoidself()
	sign = 0
	sign1 = 0
def move():
	tx = blocks[0].x
	ty = blocks[0].y
	td = blocks[0].direction
	for i in xrange (snake_len - 1, 0, -1):
		blocks[i] = blocks[i - 1]
	if td is 'a':
		blocks[0] = block(tx - 1, ty, td)
	elif td is 'w':
		blocks[0] = block(tx, ty - 1, td)
	elif td is 'd':
		blocks[0] = block(tx + 1, ty, td)
	else :
		blocks[0] = block(tx, ty + 1, td)

def snake_init():
	global alive
	for i in range (1, snake_len + 1):
		blocks.append(block(i + 70, 50, 'a'))
	alive = 1
	screen.fill((225,225,225))
	
def judge():
	global alive
	tx = blocks[0].x
	ty = blocks[0].y
	if tx < 0 or tx >= 100 or ty < 0 or ty >= 100:
		alive = 0
	for i in range (1, snake_len):
		if tx is blocks[i].x and ty is blocks[i].y:
			alive = 0


def snake_show():
	for _block in blocks:
		pygame.draw.rect(screen, (100, 100, 150), _block.rect, 0)

def act():
	global alive
	global snake_len
	global blocks
	judge()
	if alive is 1:
		screen.fill((225,225,225))
		eat()
		spawn()
		ai()
#		avoidself()
		move()
		snake_show()
	else:
		pass
	#	del blocks[:]
	#	alive = 1
	#	snake_len = 45
	#	snake_init()

#-------------------------
#func   use

snake_init()
#-------------------------
#test zone

#-------------------------
#render zone

#-------------------------
#main
while True:
	for event in pygame.event.get():
		tx = blocks[0].x
		ty = blocks[0].y
		td = blocks[0].direction
		if event.type == QUIT:
			exit()
		if event.type == KEYDOWN:
			if event.key is K_w and td is not 's':
				blocks[0] = block(tx, ty, 'w')
			elif event.key is K_d and td is not 'a':
				blocks[0] = block(tx, ty, 'd')
			elif event.key is K_a and td is not 'd':
				blocks[0] = block(tx, ty, 'a')
			elif event.key is K_s and td is not 'w':
				blocks[0] = block(tx, ty, 's')

	act()
	print snake_len
	#clock.tick(FPS)
	pygame.display.update()

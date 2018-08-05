import pygame, sys, math
import pygame.draw, pygame.font
from PIL import Image
import numpy as np
import os
import subprocess

pygame.init()

# original (powder blue background, blue lines)
# background_color = (211,255,252)
# line_color = (74,129,255)
# x_axis_color = (142,179,163)
# y_axis_color = (175,230,226)

# blueprint (blue background, robin's egg lines)
background_color = (74,129,255)
line_color =  (211,255,252)
x_axis_color = y_axis_color = (175,230,226)

size = (356, 255)

ymin = -1.4
ymax = 1.4

xmin = -1.95
xmax = 1.95

# screen = pygame.display.set_mode(size)
surf = pygame.Surface(size)

font = pygame.font.Font('../pixelmix-8px.ttf', 8)

def map_range(value, in_min, in_max, out_min, out_max):
	slope = (out_max - out_min) / (in_max - in_min)
	return out_min + slope * (value - in_min)

def real_y_to_screen_y(y, mn, mx):
#	return int(round((ymax - y) * size[1] / (ymax - ymin)))
	norm = map_range(y, mn, mx, -1.0, 1.0) * -1
	return int(map_range(norm, -1.0, 1.0, 0, size[1]))

def screen_y_to_real_y(y, mn, mx):
	norm = map_range(y, 0, size[1], -1.0, 1.0) * -1
	return map_range(norm, -1.0, 1.0, mn, mx)
	
def real_x_to_screen_x(x, mn, mx):
	return int(map_range(x, mn, mx, 0, size[0]))
	
def screen_x_to_real_x(x, mn, mx):
	return map_range(x, 0, size[0], mn, mx)

def text(surf, content, x, y, color):
	text_surface = font.render(content, False, color)
	surf.blit(text_surface, (x, y))

def h_tick(surf, x, y, color, content):
	x0 = real_x_to_screen_x(x, xmin, xmax)
	l = 5
	y0 = real_y_to_screen_y(y, ymin, ymax)
	pygame.draw.line(
		surf, y_axis_color,
		(x0 + l, y0),
		(x0 - l, y0)
	)
	text(surf, content, x0 + l + 4, y0 - 4, color)

def watermark(surf):
	text(surf, 'paulherz.com', size[0]-70, size[1]-15, x_axis_color)

def graph_background(surf):
	surf.fill(background_color)
	watermark(surf)
	# solid y-axis line
	mid = int(round(size[0] / 2))
	pygame.draw.line(
		surf, y_axis_color, 
		(mid, 0),
		(mid, size[1])
	)
	# 1.0 and -1.0 ticks
	h_tick(surf, 0, 1.0, y_axis_color, '1.0')
	h_tick(surf, 0, -1.0, y_axis_color, '-1.0')
	# dotted x-axis line
	for x in range(0, size[0], 2):
		surf.set_at((x, real_y_to_screen_y(0, ymin, ymax)), x_axis_color)

def real_plot(surf, function, base_x):
	x_step = (xmin - xmax) / size[0]
	x_offset = base_x * x_step
	for i in range(size[0] - 1):
		x_range = (xmin - x_offset, xmax - x_offset)
		x1 = screen_x_to_real_x(i,   *x_range)
		x2 = screen_x_to_real_x(i+1, *x_range)
		y1 = real_y_to_screen_y(line_function(x1), ymin, ymax)
		y2 = real_y_to_screen_y(line_function(x2), ymin, ymax)
		
		pygame.draw.line(
			surf, line_color,
			(i, y1),
			(i, y2)
		)

def list_plot(surf, ls, base_x):
	for i in range(size[0] - 1):
		x1 = (i + base_x) % len(ls)
		x2 = (i+1 + base_x) % len(ls)
		y1 = real_y_to_screen_y(ls[x1], ymin, ymax)
		y2 = real_y_to_screen_y(ls[x2], ymin, ymax)
		
		# lines only need to travel to the y-position
		# adjacent to the next point's y position
		# (this reduces overlap)
		if y1 > y2:
			y2 += 1
		elif y1 < y2:
			y2 -= 1
		
		pygame.draw.line(
			surf, line_color,
			(i, y1),
			(i, y2)
		)
		
def surf_to_png(surf, size, path):
	data = pygame.image.tostring(surf, 'RGBA')
	img = Image.frombytes('RGBA', size, data)
	img.save(path, 'PNG')
	
def list_plot_frames(size, ls, bx, p, move_speed=1):
	surf = pygame.Surface(size)
	try:
		os.mkdir(p)
	except FileExistsError:
		pass
	for i, y in list(enumerate(ls))[::move_speed]:
		filename = os.path.join(p, f'{i:04}.png')
		graph_background(surf)
		list_plot(surf, ls, bx + i)
		surf_to_png(surf, size, filename)
	# number of frames
	return len(ls)

sine_wave = np.sin(np.linspace(0, math.tau, 100))[1:]
square_wave = []
for v in sine_wave:
	if v > 0:
		square_wave.append(1)
	else:
		square_wave.append(-1)

saw_range = abs(
	real_y_to_screen_y(1,ymin,ymax) 
	- real_y_to_screen_y(-1,ymin,ymax)
)
sawtooth_wave = np.linspace(-1, 1, saw_range)

triangle_wave = np.abs(sawtooth_wave) * 2 - 1

equations = {
	'sine': sine_wave,
	'square': square_wave,
	'saw': sawtooth_wave,
	'triangle': triangle_wave
}

for name, equation in equations.items():
	# make raw frames
	list_plot_frames(size, equation, 0, f'frames/{name}', move_speed=2)
"""
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: 
			sys.exit()
	
	graph_background(surf)
	list_plot(surf, ls, base_x)
		
	screen.blit(surf, surf.get_rect())
	pygame.display.flip()
	
	base_x += 1
"""
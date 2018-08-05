import pygame, sys, math, os
import pygame.draw, pygame.font
from PIL import Image
import os.path, sys
import json

with open('howtomakeasound-u8-8000hz.raw','rb') as f:
	samples = f.read()

pygame.init()

# screen space is y-invert (0 at the top)
# so we need to define what that top corresponds to
# in the space of the chart.
ymax = 255

background_color = (0,0,0)
line_color = (200,200,200)
text_color = (255,255,255)

# load some basic project-wide parameters from file
with open('../settings.json') as json_data:
	settings = json.load(json_data)
	size = (settings['width'], settings['height'])

# positive numbers move the chart down
# (approximately center on screen by taking half of canvas
# height and subtracting roughly half of chart height)
y_offset = int(size[1] / 2) - int(ymax / 2)

# xscale is an integer representing the number of samples
# plotted in a single y-column in screen space (smush factor)
xscale = int(round(len(samples) / size[0]))

surf = pygame.Surface(size)
surf.fill(background_color)

# load the bitmap font
font = pygame.font.Font(
	os.path.join(os.getcwd(), '../pixelmix-8px.ttf'), 16
)

# print the spoken text transcript to screen
# with hand-spacing to match up to parts of the
# sound wave
text_surface = font.render(
	' how   to   make  a            sound', 
	False, text_color
)
surf.blit(text_surface, (25, 0.7 * size[1]))

screen_points = [ymax - y + y_offset for y in samples]

# hackish way to turn [a,b,c,d,e,f,g] into [(a,b,c),(d,e,f)...]
# for a given chunk size (here, `xscale`)
chunks = list(zip(*[iter(screen_points)]*xscale))

# draw a line from the minimum to the maximum value contained
# within a single y-column.
for x, chunk in enumerate(chunks):
	mn, mx = min(chunk), max(chunk)
	pygame.draw.line(surf, line_color, (x, mn), (x, mx))

preview_mode = '--preview' in sys.argv[1:]
if preview_mode:
	# show the image rendered in a window
	screen = pygame.display.set_mode(size)
	screen.blit(surf, surf.get_rect())
	pygame.display.flip()
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: 
				sys.exit()
else:
	# save the photo to file
	data = pygame.image.tostring(surf, 'RGB')
	img = Image.frombytes('RGB', size, data)
	img.save('out/title-unoptimized.png', 'PNG')
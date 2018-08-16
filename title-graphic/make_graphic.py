import pygame, sys, math, os
import pygame.draw, pygame.font
from PIL import Image
import os.path, sys
import json

preview_mode = '--preview' in sys.argv[1:]

if not preview_mode and len(sys.argv) != 3:
	print('''
	usage: 
	make_graphic.py [audio_file] [out_file]
	    
	    generates an image of the waveform with text annotation and saves to
	    a PNG file.

	    audio_file: a raw, unsigned 8-bit audio waveform at 8000Hz sample rate
	    out_file:   the location to save the waveform image to.

	make_graphic.py --preview

	    previews the graphic in a window without committing to file.
	''')
elif not preview_mode:
	in_file_name = sys.argv[1]
	out_file_name = sys.argv[2]

with open(in_file_name,'rb') as f:
	samples = f.read()

pygame.init()

# screen space is y-invert (0 at the top)
# so we need to define what that top corresponds to
# in the space of the chart.
ymax = 255

background_color = (0,0,0)
line_color = (200,200,200)
text_color = (255,255,255)

size = (500, 358)

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
	img.save(out_file_name, 'PNG')
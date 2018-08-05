import pygame, sys, math
import pygame.draw, pygame.font
from PIL import Image


with open('/Users/phrz/Notebooks/howtomakeasound-spoken.raw','rb') as f:
	samples = list(map(lambda x: x, f.read()))

pygame.init()

xscale = 24
ymax = 255
line_color = (200,200,200)
text_color = (255,255,255)
size = (len(samples) // xscale, 255)

screen = pygame.display.set_mode(size)
surf = pygame.Surface(size)
surf.fill((0,0,0))

font = pygame.font.Font('/Users/phrz/Library/Fonts/hellovetica.ttf', 8)
text_surface = font.render(
	'how     to       make    a                 sound', 
	False, text_color
)
surf.blit(text_surface, (25,180))

previous = (0, samples[0])
for i, sample in enumerate(samples[1:]):
	current = i // xscale, ymax - sample
	pygame.draw.line(surf, line_color, previous, current)
	previous = current

screen.blit(surf, surf.get_rect())
pygame.display.flip()

data = pygame.image.tostring(surf, 'RGBA')
img = Image.frombytes('RGBA', size, data)
img.save('/Users/phrz/Desktop/image.png', 'PNG')

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: 
			sys.exit()
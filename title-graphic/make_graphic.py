import pygame, sys, math, os
import pygame.draw, pygame.font
from PIL import Image
import os.path

with open('howtomakeasound-u8-8000hz.raw','rb') as f:
	samples = f.read()

pygame.init()

xscale = 24
ymax = 255
line_color = (200,200,200)
text_color = (255,255,255)
size = (len(samples) // xscale, 255) # 365

surf = pygame.Surface(size)
surf.fill((0,0,0))

font = pygame.font.Font(
	os.path.join(os.getcwd(), '../pixelmix-8px.ttf'), 8
)

text_surface = font.render(
	'how     to       make     a                 sound', 
	False, text_color
)
surf.blit(text_surface, (25,180))

previous = (0, samples[0])
for i, sample in enumerate(samples[1:]):
	current = i // xscale, ymax - sample
	pygame.draw.line(surf, line_color, previous, current)
	previous = current

data = pygame.image.tostring(surf, 'RGB')
img = Image.frombytes('RGB', size, data)
img.save('out/title-unoptimized.png', 'PNG')
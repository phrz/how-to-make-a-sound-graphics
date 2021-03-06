'''
expects a file called table_frames.txt, containing a series of <f> objects.
Yes, this means there is a leading pipe.

<f>: "|" + <blob>
<blob>: valid data URI format for a PNG ("data:image/png;base64,...")
'''

from PIL import Image
import base64
from io import BytesIO

import sys
import os.path

# .
base_dir = sys.argv[1]
# ./frames
frames_dir = os.path.join(base_dir, 'frames')
# ./table_frames.txt
table_frames_file = os.path.join(base_dir, 'table_frames.txt')

def strip_prefix(s, prefix):
	if s[:len(prefix)] == prefix:
		return s[len(prefix):]
	return s

with open(table_frames_file,'r') as f:
	data = f.read()

blobs = data.split('|')
blobs = filter(lambda x: len(x) != 0, blobs)

for i, blob in enumerate(blobs):
	encoded_data = strip_prefix(blob, 'data:image/png;base64,')
	image_data = base64.standard_b64decode(encoded_data)
	image_file = BytesIO(image_data)
	image = Image.open(image_file)

	out_file = os.path.join(frames_dir, f'{i:04}.png')
	image.save(out_file, 'PNG')
	
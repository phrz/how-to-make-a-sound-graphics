# WAVE TABLE

BLOBS_TARGET="table_frames.txt"

default: animated_gif

setup:
	brew install apng2gif pngcrush
	pip3 install --user pipenv

folders:
	mkdir -p out
	mkdir -p frames/crushed

${BLOBS_TARGET}: folders
	pipenv run python3 make_blobs.py

frames: ${BLOBS_TARGET} folders
	pipenv run python3 blobs_to_files.py

crushed_frames: frames
	sh crush_frames.sh

animated_png: crushed_frames
	sh make_apng.sh

animated_gif: animated_png
	sh make_gif.sh

clean:
	rm -rf frames out
	rm table_frames.txt
# BOUNCING BALL

BLOBS_TARGET="ball_frames.txt"

default: animated_gif

setup:
	brew install apng2gif parallel
	pip3 install --user pipenv

folders:
	mkdir -p out
	mkdir -p frames/crushed

${BLOBS_TARGET}: folders
	pipenv run python3 make_blobs.py

frames: ${BLOBS_TARGET} folders
	pipenv run python3 blobs_to_files.py

animated_png: frames
	sh make_apng.sh

animated_gif: animated_png
	sh make_gif.sh

clean:
	rm -rf frames out
	rm ball_frames.txt
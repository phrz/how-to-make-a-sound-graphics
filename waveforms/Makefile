default: animated_gifs

setup:
	brew install apng2gif
	pip3 install --user pipenv
	pipenv --python 3.7

folders:
	mkdir -p out
	mkdir -p frames

frames: folders
	pipenv run python3 make_frames.py

crushed_frames: frames
	sh crush_frames.sh

animated_pngs: crushed_frames
	sh make_apngs.sh

animated_gifs: animated_pngs
	sh make_gifs.sh

clean:
	rm -rf frames out
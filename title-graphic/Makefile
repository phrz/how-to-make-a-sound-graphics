default: out/title.png

setup:
	brew install pngquant
	pip3 install --user pipenv

folders:
	mkdir -p out

preview:
	pipenv run python3 make_graphic.py --preview

out/title-unoptimized.png: folders
	pipenv run python3 make_graphic.py

out/title.png: out/title-unoptimized.png
	pngquant 3 out/title-unoptimized.png --ext -png8.png
	mv out/title-unoptimized-png8.png out/title.png

clean:
	rm -rf out
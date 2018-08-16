# PROPERTIES
###############################################
# - global
FONT_FILE = pixelmix-8px.ttf

# - title graphic
TITLE_BASE = title-graphic/
TITLE_OUT_DIR = $(TITLE_BASE)out/

TITLE_FOLDERS = $(TITLE_OUT_DIR)

TITLE_SOUND_FILE = $(TITLE_BASE)howtomakeasound-u8-8000hz.raw
TITLE_GENERATOR = $(TITLE_BASE)make_graphic.py

TITLE_OUT_UNOPT = $(TITLE_OUT_DIR)title-unoptimized.png
TITLE_OUT = $(TITLE_OUT_DIR)title.png

# - wave table
TABLE_BASE = wave-table/
TABLE_FRAMES_DIR = $(TABLE_BASE)frames/
TABLE_OUT_DIR = $(TABLE_BASE)out/

TABLE_FOLDERS = $(TABLE_FRAMES_DIR) $(TABLE_OUT_DIR)

# stand in for all frames, bc the number can be adjusted
TABLE_FRAMES = $(TABLE_FRAMES_DIR)0000.png

TABLE_BLOB_FILE = $(TABLE_BASE)table_frames.txt

TABLE_FILE_NAME = wave_table
TABLE_APNG_FILE = $(TABLE_OUT_DIR)$(TABLE_FILE_NAME).png
TABLE_GIF_FILE = $(TABLE_OUT_DIR)$(TABLE_FILE_NAME).gif

TABLE_FPS = 25

# - waveforms
WAVE_BASE = waveforms/
WAVE_FRAMES_DIR = $(WAVE_BASE)frames/
WAVE_OUT_DIR = $(WAVE_BASE)out/

WAVE_FRAME_GENERATOR = $(WAVE_BASE)make_frames.py

WAVE_FOLDERS = \
$(addprefix $(WAVE_FRAMES_DIR), $(WAVE_FORMS)) \
$(WAVE_OUT_DIR)

WAVE_FRAMES_TARGET = $(WAVE_FRAMES_DIR)%/0000.png

WAVE_FORMS = saw sine square triangle

# MAKEFILE CONFIGURATION
###############################################
.DEFAULT_GOAL := all
.PHONY: title_preview \
title_default table_default wave_default \
title_clean table_clean wave_clean \
all setup clean

# prevent frames from being deleted
# prevent APNGs from being deleted when making GIFs
.PRECIOUS: $(WAVE_FRAMES_TARGET) $(WAVE_OUT_DIR)%.png

# ALL PURPOSE TASKS
###############################################
all: title_default table_default wave_default
clean: title_clean table_clean wave_clean

setup:
	brew install pngcrush apng2gif
	pip3 install --user pipenv
	pipenv install
	mkdir -p $(TITLE_FOLDERS) $(WAVE_FOLDERS) $(WAVE_FOLDERS)

# TITLE GRAPHIC TASKS
###############################################

title_default: $(TITLE_OUT)

title_preview:
	pipenv run python3 $(TITLE_GENERATOR) $(FONT_FILE) --preview

$(TITLE_OUT_UNOPT): $(TITLE_FOLDERS)
	pipenv run python3 $(TITLE_GENERATOR) \
	$(FONT_FILE) $(TITLE_SOUND_FILE) $(TITLE_OUT_UNOPT)

$(TITLE_OUT): $(TITLE_OUT_UNOPT)
	pngcrush $(TITLE_OUT_UNOPT) $(TITLE_OUT)

title_clean:
	-rm -r ./$(TITLE_BASE)out/*

# WAVE TABLE TASKS
###############################################

table_default: $(TABLE_GIF_FILE)

# this python file opens Chrome with a Three.js
# program to generate the frames in the form of
# a pipe ("|") delimited file of "data:" blobs
$(TABLE_BLOB_FILE):
	pipenv run python3 \
	$(TABLE_BASE)make_blobs.py \
	$(TABLE_BASE)table.html \
	$(TABLE_BLOB_FILE)

# this program generates individual PNG files
# from the blobs file
$(TABLE_FRAMES): $(TABLE_BLOB_FILE)
	pipenv run python3 \
	$(TABLE_BASE)blobs_to_files.py \
	$(TABLE_BASE)

# Frames -> APNG
$(TABLE_APNG_FILE): $(TABLE_FRAMES)
	cat $(TABLE_FRAMES_DIR)*.png | \
	ffmpeg -r "$(TABLE_FPS)" -y -f image2pipe \
	-i - -f apng -plays 0 $(TABLE_APNG_FILE)

# APNG -> GIF
$(TABLE_GIF_FILE): $(TABLE_APNG_FILE)
	apng2gif $(TABLE_APNG_FILE)

table_clean:
	-rm -r ./$(TABLE_OUT_DIR)* \
	./$(TABLE_FRAMES_DIR)* ./$(TABLE_BLOB_FILE)

# WAVEFORM TASKS
###############################################

WAVE_GIFS = \
$(addprefix $(WAVE_OUT_DIR), \
$(addsuffix .gif, $(WAVE_FORMS)))

wave_default: $(WAVE_GIFS)

# run the python program that generates frames
$(WAVE_FRAMES_TARGET):
	pipenv run python3 $(WAVE_FRAME_GENERATOR) \
	$(FONT_FILE) $(WAVE_FRAMES_DIR)

# Frames -> APNGs
$(WAVE_OUT_DIR)%.png: $(WAVE_FRAMES_TARGET)
	cat $(WAVE_FRAMES_DIR)$*/*.png | \
	ffmpeg -y -f image2pipe \
	-i - -f apng -plays 0 $(WAVE_OUT_DIR)$*.png

# APNGs -> GIFs
$(WAVE_OUT_DIR)%.gif: $(WAVE_OUT_DIR)%.png
	apng2gif $(WAVE_OUT_DIR)$*.png

wave_clean:
	-rm -r ./$(WAVE_FRAMES_DIR)*/* ./$(WAVE_OUT_DIR)*
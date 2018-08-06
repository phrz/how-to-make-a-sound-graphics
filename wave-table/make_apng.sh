APNG_NAME="wave_table"
APNG_PATH="out/${APNG_NAME}.png"

# default 25
FRAMES_PER_SECOND=25
cat frames/crushed/*.png | ffmpeg -r "${FRAMES_PER_SECOND}" -y -f image2pipe -i - -f apng -plays 0 $APNG_PATH
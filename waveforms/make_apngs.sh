for D in frames/*; do
	if [ -d "${D}" ]; then
		APNG_NAME="$(basename "$D")"
		APNG_PATH="out/${APNG_NAME}.png"
		cat ${D}/*.png | ffmpeg -y -f image2pipe -i - -f apng -plays 0 $APNG_PATH
	fi
done
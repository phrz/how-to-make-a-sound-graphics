for D in frames/*; do
	if [ -d "${D}" ]; then
		pngcrush -d ${D}/crushed ${D}/*.png
	fi
done
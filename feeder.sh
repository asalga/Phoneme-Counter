#!/bin/sh

# Andor Salga
# September 2014

# Notes:
# Start the MaryTTS server before running this script.
# fix voice

OUT="analysis.txt"
rm analysis.txt

while read line
do
	sleep 0.25
	
	echo "$line" >> "$OUT"

	curl localhost:59125/process -d INPUT_TEXT="$line" \
		-d INPUT_TYPE=TEXT 		\
		-d OUTPUT_TYPE=PHONEMES \
		-d LOCALE=en_US			\
		-H "Content-Type: application/x-www-form-urlencoded; charset=utf-8" | python phoneme_counter.py >> "$OUT"

	echo "\n" >> "$OUT"
	
	#echo "$TEST"

done < input.txt

#-d VOICE='cmu-rms-hmss'	\


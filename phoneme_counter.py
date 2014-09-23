# Andor Salga
# Sept 2014

# receives xml counts phonemes and returns counts of each phoneme.
#

import fileinput
import re
import sys
import math
from xml.dom import minidom
from collections import Counter

# TODO: check list
allPhonemes = [	"r=",
				"@",	"V",	"e",	"I",  "i:",  "{",  "O:",  "Q",  "U",  "u:",  
				"@r",	"eI",	"aI",	"OI",  '@U',  "aU",  "I@",  "e@",  'U@',  
				"O@",	"Q@",	"p",	"t",  "k",  "tS",  "f",  "T",  "s",  "S",  
				"h",	"ph",	"th",	"kh",   "w",  "j",  "b",  "d",  "dZ",  "v",  
				"D",	"z",	"Z",	"m",  "n",  "N",  "r",  "l",  "g",  "bh",  "dh",  "gh"];

# In a hurry, so doing this the hacky way
# generating an xml just to feed into minidom
tempXmlFile = open('temp.xml', 'w')
for line in sys.stdin:
	tempXmlFile.write(line.encode('ascii'))

tempXmlFile.close()

# Now let's count those phonemes
xmldoc = minidom.parse('temp.xml')

phonemes = []

# Each word will have an associated <t>
tags = xmldoc.getElementsByTagName('t')

for t in tags:
	if(t.hasAttribute('ph')):
		x = t.attributes['ph'].value.encode('ascii')
		
		stringPhonemes = x.split(" ")

		for r in stringPhonemes:
			# ' Occurs before each word from MaryTTS. Is it a space?
			# We don't want to include them in counts.
			if r != "'" and r != "-":
				phonemes.append(r)

test = Counter(phonemes).most_common()

# We want the output in the format:
# Some text goes here
# total characters: 6
# @		V
# 10	10
# 25%	25%	

totalPhonemes = 0
for c in test:
	totalPhonemes += float(c[1])

sys.stdout.write("total phonemes: " + str(int(totalPhonemes)) + "\n")

# Print out all the phonemes
for ph in allPhonemes:
	sys.stdout.write(ph + "\t")
sys.stdout.write("\n")

phraseDict = dict(test)

# Counts
for ph in allPhonemes:
	try:
		sys.stdout.write(str(phraseDict[ph]) + "\t")
	except KeyError:
		sys.stdout.write("0\t")
sys.stdout.write("\n")

# Percentages
for ph in allPhonemes:
	try:
		sys.stdout.write(str(round(phraseDict[ph]/totalPhonemes*100, 3)) + "%\t")
	except KeyError:
		sys.stdout.write("0%\t")
sys.stdout.write("\n")

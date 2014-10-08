# Andor Salga
# Sept 2014

# receives xml counts phonemes and returns counts of each phoneme.

import fileinput
import re
import sys
import math
from xml.dom import minidom
from collections import Counter
from collections import OrderedDict


# Given a data set, we find all the potential phonemes, place them into this
# list, then when doing counts, we lookup the values

# There seems to be different standards of phonemes, so our solution is just to extract
# all the possible phonemes from the given dataset provided.
				
allPhonemes = ['D', '@', 'I', 'k', 'A', 'n', 'm', 'i', 'z', 's', '@U', 'b', '{', 'd', 'AI', 'T', 'r', 'u', 'aU', 't', 'E', 'f', 'O', 'r=', 'EI', 'v', 'h', 'tS', 'V', 'dZ', 'l', 'w', 'j', 'OI', 'N', 'S', 'p', 'U', 'g']

# old standard
#"r=",
#				"@",	"V",	"e",	"I",  "i:",  "{",  "O:",  "Q",  "U",  "u:",  
#				"@r",	"eI",	"aI",	"OI",  '@U',  "aU",  "I@",  "e@",  'U@',  
#				"O@",	"Q@",	"p",	"t",  "k",  "tS",  "f",  "T",  "s",  "S",  
#				"h",	"ph",	"th",	"kh",   "w",  "j",  "b",  "d",  "dZ",  "v",  
#				"D",	"z",	"Z",	"m",  "n",  "N",  "r",  "l",  "g",  "bh",  "dh",  "gh"];

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
			# The  '  character occurs before each word from MaryTTS. Is it a space?
			# We don't want to include them in counts.
			if r != "'" and r != "-":
				phonemes.append(r)

uniquePhonemes = list(OrderedDict.fromkeys(phonemes))


phonemeCounts = Counter(phonemes).most_common()
# [('t', 2), ('E', 1), ('n', 1), ('s', 1), ('w', 1), ('V', 1)]

#
# Desired output format:
# Some text goes here
# total characters: 6
# @		V
# 10	10
# 25%	25%	
#


#
# 1th element will have the count for a particular phoneme.
numPhonemesInSentence = 0
for c in phonemeCounts:
	numPhonemesInSentence += float(c[1])
sys.stdout.write("total phonemes: " + str(int(numPhonemesInSentence)) + "\n")


#
# Print out all the phonemes
for ph in allPhonemes:
	sys.stdout.write(ph + "\t")
sys.stdout.write("\n")



phraseDict = dict(phonemeCounts)
# {'@': 1, 'E': 1, 'D': 1, 'I': 2, 's': 2, 't': 2, 'z': 1}


found = 0
#
# Iterate over the standard phoneme dataset
# If the iter value is found in the phraseDict, we can add the count
for ph in allPhonemes:
	try:
		sys.stdout.write(str(phraseDict[ph]) + "\t")
		found += phraseDict[ph]
	except KeyError:
		sys.stdout.write("0\t")
sys.stdout.write("\n")


#
# Percentages
# totalPercent = 0.0
for ph in allPhonemes:
	try:
		sys.stdout.write(str(round(phraseDict[ph]/numPhonemesInSentence*100, 3)) + "%\t")
	except KeyError:
		sys.stdout.write("0%\t")
sys.stdout.write("\n")
#sys.stdout.write(str(found/numPhonemesInSentence))

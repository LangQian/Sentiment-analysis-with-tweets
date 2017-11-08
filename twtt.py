#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, csv, re, urllib2
from HTMLParser import HTMLParser
import NLPlib

tagger = NLPlib.NLPlib()

# ---------------------- Pre-processing Functions ----------------------

# All html tags and attributes (i.e., /<[^>]+>/) are removed
def twtt1(input):
	return html_matcher.sub("", input)

# Html character codes (i.e., &...;) are replaced with an ASCII equivalent
def twtt2(input):
	string = urllib2.unquote(input).decode('utf8','ignore')
	return h.unescape(string).encode(sys.getfilesystemencoding())

# All URLs (i.e., tokens beginning with http or www) are removed
def twtt3(input):
	return url_matcher.sub("", input)

# The first character in Twitter user names and hash tags (i.e., @ and #) are removed
def twtt4(input):
	return tag_matcher.sub("", input)

# Each sentence within a tweet is on its own line
def twtt5(input):
	input = input.strip()
	abbrev_list = [re.sub(r"\n", "", item) for item in list(abbrev.readlines())]
	abbrev_list.extend(['e.g.', 'i.e.'])
	sentence = re.split(r'\s+', input)
	for i in range(len(sentence)):
		if re.search(r"\.",sentence[i]):
			if not(sentence[i] in abbrev_list):
				if re.search("n't.", sentence[i]):
					re.sub("n't.", "n't. \n", sentence[i])
				else: 
					if len(re.split(r"(\W+)(?=\w)", sentence[i])) < 3:
						# sentence[i] = re.split(r"(\W+)(?=\w)", sentence[i])[0] + " \n" + "".join(re.split(r"(\W+)(?=\w)", sentence[i])[1:])
						sentence[i] = sentence[i] + " \n"
					else:
						sentence[i] = "".join(re.split(r"(\W+)(?=\w)", sentence[i])[0:-1]) + " \n" + re.split(r"(\W+)(?=\w)", sentence[i])[-1]
		elif re.search(r"\!|\?",sentence[i]):
			# if sentence[i+1][0].isupper():
			sentence[i] = sentence[i] + " \n"

	if len(sentence) == 1 or len(sentence) == 0:
		pass
	elif sentence[len(sentence)-1][-1] == "\n":
		sentence[len(sentence)-1] = sentence[len(sentence)-1][0:-2]
	return re.sub(r"\n\s+", "\n", " ".join(sentence))

# Ellipsis (i.e., ‘...’), and other kinds of multiple punctuation (e.g., ‘!!!’) are not split
def twtt6(input):
	print("Already qualified in twtt5")

# Each token, including punctuation and clitics, is separated by spaces
def twtt7(input):
	abbrev_list = [re.sub(r"\n", "", item) for item in list(abbrev.readlines())]
	abbrev_list.extend(['e.g.', 'i.e.'])
	sentence = re.split(r" ", input)
	for i in range(len(sentence)):
		if re.search(r"\w\W|\W\w",sentence[i]):
			if not(sentence[i] in abbrev_list):
				if re.search(r"n't", sentence[i]):
					if re.search("n't.", sentence[i]):
						sentence[i] = re.sub("n't.", "n't .", sentence[i])
					sentence[i] = re.sub("n't", " n't", sentence[i])
				elif re.search(r"\n", sentence[i]):
					sentence[i] = " ".join(re.split(r"(\W+)(?=\w)", sentence[i]))
					sentence[i] = " ".join(re.split(r"(?<=\w)(\W+)", sentence[i]))
				elif re.search(r"\$\d", sentence[i]):
					sentence[i] = " ".join(re.split(r'(\$)', sentence[i]))
				elif re.search(r"\d\W\d", sentence[i]):
					pass
				else:
					sentence[i] = re.split(r'(\W)', sentence[i])[0] + " " + "".join(re.split(r'(\W)', sentence[i])[1:])
	return " ".join(sentence)

# Each token is tagged with its part-of-speech
def twtt8(input):
	global tagger
	sentence = re.split(r' ', input)
	tags = tagger.tag(sentence)
	result = []
	for word, tag in zip(sentence, tags):
		result.append(word + "/" + tag)
	return re.sub(r"\n/NN ", "\n", re.sub(r" /NN", "", " ".join(result)))

# Before each tweet is demarcation ‘<A=#>’, which occurs on its own line, where # is the numeric class of the tweet (0 or 4)
def twtt9(input, polarity):
	pol = "<A=" + polarity + ">\n"
	result = pol + input
	return result

# ---------------------- Main Function ----------------------

def main(input_file, student_id, output_file):

	#check if input args are valid
	try:
		id = int(student_id)
	except:
		print("Please input a valid student ID.")

	start_pos1 = id % 80 * 10000
	start_pos2 = 800000 + start_pos1

	with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
		raw = csv.reader(infile)
		data = list(raw)
		if output_file == 'test.twt':
			print(len(data))
			for line in data:
				outfile.write(twtt9(twtt8(twtt7(twtt5(twtt4(twtt3(twtt2(twtt1(line[5].strip()))))))), line[0]))
				outfile.write("\n")
		else:
			for line in data[start_pos1 : start_pos1+10000]:
				outfile.write(twtt9(twtt8(twtt7(twtt5(twtt4(twtt3(twtt2(twtt1(line[5].strip()))))))), line[0]))
				outfile.write("\n")
			for line in data[start_pos2 : start_pos2+10000]:
				outfile.write(twtt9(twtt8(twtt7(twtt5(twtt4(twtt3(twtt2(twtt1(line[5].strip()))))))), line[0]))
				outfile.write("\n")

if __name__ == "__main__":
	
	h = HTMLParser()

	htmlCase = r'<[^>]+>'
	html_matcher = re.compile(htmlCase)

	urlCase = r"http\S+|www\S+|Http\S+|WWW\S+"
	url_matcher = re.compile(urlCase)

	tagCase = r"@|#"
	tag_matcher = re.compile(tagCase)

	with open("../Wordlists/abbrev.english", 'r') as abbrev:
		# check if the number of input args is 3
		try:
			main(sys.argv[1], sys.argv[2], sys.argv[3])
		except:
			print("Valid Format: python twtt.py [input_filename] [Student ID] [output_filename]")
		# test = 'Http://bit.ly/PACattack'
		# # print twtt8(twtt7(twtt5(twtt4(twtt3(twtt2(twtt1(test)))))))
		# print twtt9(twtt8(twtt7(twtt5(twtt4(twtt3(twtt2(twtt1(test))))))), '0')
	# print twtt8("sdjfh jaskfjd , jhj she i 've said, she 's are n't ! $ 100,000. ? dogs ' ' something good ' ??? ... j s")
	# test = 'Meet me today at the FEC in DC at 4. Wear a carnation so I know it’s you. <a href="Http://bit.ly/PACattack" target="_blank" class="tweet-url web" rel="nofollow">Http://bit.ly/PACattack</a>.'
	# print twtt9(twtt8(twtt7(twtt5(twtt4(twtt3(twtt2(twtt1(test))))))), '0')
	#print(twtt1('<p>Http://bit.ly/PACattack</p>'))
	
	
	
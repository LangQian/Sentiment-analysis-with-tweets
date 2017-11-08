#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, re, string

# ---------------------- Counting Part ----------------------

# — First person pronouns (feat1)
def feat1(input):
	num = 0
	with open('../Wordlists/First-person', 'r') as reference:
		ref_list = [item.lower() for item in [re.sub(r"\n", "", item) for item in list(reference.readlines())]]
		tokens = re.split(r'\s+', input)
		for token in tokens:
			if re.split(r"/", token)[0].lower() in ref_list:
				num += 1
	return num

# — Second person pronouns (feat2)
def feat2(input):
	num = 0
	with open('../Wordlists/Second-person', 'r') as reference:
		ref_list = [item.lower() for item in [re.sub(r"\n", "", item) for item in list(reference.readlines())]]
		tokens = re.split(r'\s+', input)
		for token in tokens:
			if re.split(r"/", token)[0].lower() in ref_list:
				num += 1
	return num

# — Third person pronouns (feat3)
def feat3(input):
	num = 0
	with open('../Wordlists/Third-person', 'r') as reference:
		ref_list = [item.lower() for item in [re.sub(r"\n", "", item) for item in list(reference.readlines())]]
		tokens = re.split(r'\s+', input)
		for token in tokens:
			if re.split(r"/", token)[0].lower() in ref_list:
				num += 1
	return num

# — Coordinating conjunctions (feat4)
def feat4(input):
	num = 0
	with open('../Wordlists/Conjunct', 'r') as reference:
		ref_list = [item.lower() for item in [re.sub(r"\n", "", item) for item in list(reference.readlines())]]
		ref_list.extend(["and", "but", "for", "nor", "or", "so", "yet"])
		tokens = re.split(r'\s+', input)
		for token in tokens:
			if re.split(r"/", token)[0].lower() in ref_list:
				num += 1
	return num

# — Past-tense verbs (feat5)
def feat5(input):
	num = 0
	tokens = re.split(r'\s+', input)
	for token in tokens:
		if token != '':
			if re.split(r"/", token)[1] in ['VBD', 'VBN']:
				num += 1
	return num

# — Future-tense verbs (feat6)
def feat6(input):
	num = 0
	tokens = re.split(r'\s+', input)
	for i in range(len(tokens)):
		if re.split(r"/", tokens[i])[0].lower() in ["'ll", "will", "gonna", "shall"]:
			num += 1
		elif i < len(tokens) - 2 and \
			re.split(r"/", tokens[i])[0].lower() == 'going' and \
			re.split(r"/", tokens[i+1])[0].lower() == 'to' and \
			re.split(r"/", tokens[i+2])[1] == 'VB':
			num += 1
	return num

# — Commas (feat7)
def feat7(input):
	num = 0
	tokens = re.split(r'\s+', input)
	for token in tokens:
		if re.search(r',', re.split(r"/", token)[0]):
			num += 1
	return num

# — Colons and semi-colons (feat8)
def feat8(input):
	num = 0
	tokens = re.split(r'\s+', input)
	for token in tokens:
		if re.split(r"/", token)[0] in [';', ':']:
			num += 1
	return num

# — Dashes (feat9)
def feat9(input):
	num = 0
	tokens = re.split(r'\s+', input)
	for token in tokens:
		if re.search(r'-', re.split(r"/", token)[0]):
			num += 1
	return num

# — Parentheses (feat10)
def feat10(input):
	num = 0
	tokens = re.split(r'\s+', input)
	for token in tokens:
		if re.search(r'\(|\)', re.split(r"/", token)[0]):
			num += 1
	return num

# — Ellipses (feat11)
def feat11(input):
	num = 0
	tokens = re.split(r'\s+', input)
	for token in tokens:
		if re.search(r'\.\.+', re.split(r"/", token)[0]):
			num += 1
	return num

# — Common nouns (feat12)
def feat12(input):
	num = 0
	tokens = re.split(r'\s+', input)
	for token in tokens:
		if token != '':
			if re.split(r"/", token)[1] in ['NN', 'NNS']:
				num += 1
	return num

# — Proper nouns (feat13)
def feat13(input):
	num = 0
	tokens = re.split(r'\s+', input)
	for token in tokens:
		if token != '':
			if re.split(r"/", token)[1] in ['NNP', 'NNPS']:
				num += 1
	return num

# — Adverbs (feat14)
def feat14(input):
	num = 0
	tokens = re.split(r'\s+', input)
	for token in tokens:
		if token != '':
			if re.split(r"/", token)[1] in ['RB', 'RBR', 'RBS']:
				num += 1
	return num

# — wh-words (feat15)
def feat15(input):
	num = 0
	tokens = re.split(r'\s+', input)
	for token in tokens:
		if token != '':
			if re.split(r"/", token)[1] in ['WDT', 'WP', 'WP$', 'WRB']:
				num += 1
	return num

# — Modern slang acronyms (feat16)
def feat16(input):
	num = 0
	with open('../Wordlists/Slang', 'r') as reference:
		ref_list = [item.lower() for item in [re.sub(r"\n", "", item) for item in list(reference.readlines())]]
		tokens = re.split(r'\s+', input)
		for token in tokens:
			if re.split(r"/", token)[0].lower() in ref_list:
				num += 1
	return num

# — Words all in upper case (at least 2 letters long) (feat17)
def feat17(input):
	num = 0
	tokens = re.split(r'\s+', input)
	for token in tokens:
		if re.split(r"/", token)[0].isupper() and len(re.split(r"/", token)[0]) > 1:
			num += 1
	return num

# ---------------------- Length Part ----------------------

# Average length of sentences (in tokens) (feat18)
def feat18(input):
	num_sentences = len(re.split(r'\n', input)) - 1
	num_tokens = len(re.split(r'\s+', input)) - 1
	return num_tokens//num_sentences


# Average length of tokens, excluding punctuation tokens (in characters) (feat19)
def feat19(input):
	count = lambda l1, l2: len(list(filter(lambda c: c in l2, l1)))
	num_tokens = 0
	num_characters = 0
	tokens = re.split(r'\s+', input)
	for i in range(len(tokens) - 1):
		token = re.split(r"/", tokens[i])[0]
		num_chars = count(token, string.ascii_letters)
		num_punct = count(token, string.punctuation)
		if num_punct == len(token):
			continue
		else:
			num_tokens += 1
			num_characters += num_chars
	return num_characters//num_tokens

#  Number of sentences (feat20)
def feat20(input):
	return len(re.split(r'\n', input)) - 1

# ---------------------- Main Function ----------------------

def main(input_file, output_file, num_tweets = 20000):

	with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:

		# --------------- Create Format ------------------------
		outfile.write('@relation tweet\n\n')
		for i in range(20):
			outfile.write('@attribute feat%d numeric\n' %(i+1))
		outfile.write('@attribute class {0, 4}\n')
		outfile.write('\n@data\n')

		# ---------------- Insert Data -------------------------
		tweets = infile.read()
		tweet_list = re.split(r'(<A=\d>\n)', tweets)
		num_of_tweet = (len(tweet_list) - 1) / 2
		class0_flag = 0
		class4_flag = 0
		for i in range(0, num_of_tweet):
			label = tweet_list[1+2*i][3]

			# ---------- Check if reach the max_number -----
			if label == '0':
				class0_flag += 1
				if class0_flag > int(num_tweets):
					continue
			elif label == '4':
				class4_flag += 1
				if class4_flag > int(num_tweets):
					continue

			tweet = tweet_list[2+2*i]

			outfile.write('%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d\n'%(\
							feat1(tweet),feat2(tweet),feat3(tweet),feat4(tweet),feat5(tweet),\
							feat6(tweet),feat7(tweet),feat8(tweet),feat9(tweet),feat10(tweet),\
							feat11(tweet),feat12(tweet),feat13(tweet),feat14(tweet),feat15(tweet),\
							feat16(tweet),feat17(tweet),feat18(tweet),feat19(tweet),feat20(tweet),\
							int(label)))

if __name__ == "__main__":
	# check if the input args are valid
	len_arg = len(sys.argv)
	if  len_arg < 3 or len_arg > 4:
		print "Usage: python buildarff.py [input_filename] [output_filename] [number_of_tweets]"
		sys.exit (1)
	if len_arg == 3:
		main(sys.argv[1], sys.argv[2])
	elif len_arg == 4:
		main(sys.argv[1], sys.argv[2], sys.argv[3])
	
	
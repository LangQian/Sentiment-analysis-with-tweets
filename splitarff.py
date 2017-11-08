#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, re, string


# ---------------------- Main Function ----------------------

def main():

	with open('train.arff', 'r') as infile:

		# ---------------- Insert Data -------------------------
		lines = infile.readlines()
		with open('../../weka-3-8-1/train_train.arff', 'w') as outfile:
			outfile.write('@relation tweet\n\n')
			for i in range(20):
				outfile.write('@attribute feat%d numeric\n' %(i+1))
			outfile.write('@attribute class {0, 4}\n')
			outfile.write('\n@data\n')
			outfile.writelines(lines[0:9000])
			#outfile.writelines(lines[9000:10000])
			outfile.writelines(lines[10000:19000])
			#outfile.writelines(lines[19000:20000])
		with open('../../weka-3-8-1/train_test.arff', 'w') as outfile:
			outfile.write('@relation tweet\n\n')
			for i in range(20):
				outfile.write('@attribute feat%d numeric\n' %(i+1))
			outfile.write('@attribute class {0, 4}\n')
			outfile.write('\n@data\n')
			outfile.writelines(lines[9000:10000])
			outfile.writelines(lines[19000:20000])

if __name__ == "__main__":
	main()
	
	
from nltk.corpus import PlaintextCorpusReader
from sklearn import cross_validation
import numpy as np
import re, nltk

bijankhan_root = '/home/server/pltk/data/'
bijankhan_fileid = 'bijankhan.txt'

def raw():
	"""
		Returns raw text of corpus
		
		>>> raw()[:54]
		'#                                                 DELM'
	"""		
	wordlists = PlaintextCorpusReader(bijankhan_root, bijankhan_fileid)
	return wordlists.raw(bijankhan_fileid)

def sents(add_pos=False, separator='/'):
	"""
		Returns list of sentences (with or without pos tags)
		:param add_pos 	 (optionally): 	add pos of each word in return sentence (DEFAULT: False)
		:param separator (optionally): 	character used for separate word and its pos tag (DEFAULT: /) 
	
		>>> len(list(sents()))
		88137
	"""
	lines = open(bijankhan_root + bijankhan_fileid).readlines()
	newLine = True
	sentence = []
	for line in lines:
		line = line.strip('\r\n')
		words = re.split(" +", line)

		if (words[0] == '#'):
			if (newLine == False):
				yield ''.join(sentence)
				sentence = []
			newLine = True
		else:
			if (newLine == False):
				sentence += [" "]
			sentence += ["_".join(words[0:len(words)-1])]
			if (add_pos == True):
				sentence += [separator + words[len(words)-1]]
			newLine = False
			if (words[0] == '.' and words[len(words)-1] == 'DELM'):
				newLine = True
				yield ''.join(sentence)
				sentence = []

def export_sents(output, add_pos=False, separator='/'):
	"""
		Returns list of sentences (with or without pos tags)
		:param output: 					output file path
		:param add_pos 	 (optionally): 	add pos of each word in return sentence (DEFAULT: False)
		:param separator (optionally): 	character used for separate word and its pos tag (DEFAULT: /) 

		>>> export_sents('/home/server/pltk/data/bijankhan-sents.txt')
		>>> export_sents('/home/server/pltk/data/bijankhan-sents-gold-tag.txt', True)
		"""
	out = open(output, 'w')
	for sent in sents(add_pos, separator):
		out.write(sent + "\n")

def split_train_test(separator='/', test_size=0.25):
	"""
		>>> train, test = split_train_test()
		>>> print(str(len(train)) + ' training data, ' + str(len(test)) + ' test data')
	"""
	setences = list(sents(True, separator))
	return cross_validation.train_test_split(setences, test_size=test_size)

def export_train_test(train_file, test_file, separator='/', test_size=0.25):
	"""
		>>> export_train_test('/home/server/pltk/data/bijankhan-train.txt', '/home/server/pltk/data/bijankhan-test.txt')
	"""
	train_set, test_set = split_train_test(separator, test_size)

	train_out = open(train_file, 'w')
	for sent in train_set:
		train_out.write(sent + "\n")

	test_out = open(test_file, 'w')
	for sent in test_set:
		test_out.write(sent + "\n")
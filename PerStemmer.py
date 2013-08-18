from nltk.stem.api import StemmerI
import os, sys, string

class PerStemmer(StemmerI):
	"""docstring for Stemmer"""
		
	def stem(self, token):
		cmd = 'echo ' + token + ' | perl perstem.pl --stem -i utf8 -o utf8'
		os.system(cmd)

	def stemText(self, sentence):
		cmd = 'echo ' + sentence + ' | perl perstem.pl --stem -i utf8 -o utf8'
		os.system(cmd)
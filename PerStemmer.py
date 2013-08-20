# coding=utf8

from nltk.stem.api import StemmerI
import os, sys, string, subprocess

class PerStemmer(StemmerI):
	"""docstring for Stemmer"""
		
	def stem(self, token):
		perstem = subprocess.Popen(['perl','perstem.pl', '--stem', '-i', 'utf8', '-o', 'utf8'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
		(data, errs) = perstem.communicate(token)
		return data

	def stemText(self, text):
		return self.stem(text)
		
		


# coding=utf8

from nltk.stem.api import StemmerI
import os, subprocess

class PerStemmer(StemmerI):
	""" perstem interface """

	script = os.path.dirname(__file__) + '/perstem.pl'

	def stem(self, token):
		perstem = subprocess.Popen(['perl', self.script, '--stem', '-i', 'utf8', '-o', 'utf8'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
		(data, errs) = perstem.communicate(token)
		return data

	def stemText(self, text):
		return self.stem(text)

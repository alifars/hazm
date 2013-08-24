# from nltk.stem.api import StemmerI
import sys
sys.path.append('/usr/lib/ironpython/DLLs')
sys.path.append('/usr/lib/python2.7')
import string, clr
clr.AddReference("./SCICT.PersianTools.dll")
clr.AddReference("./SCICT.NLP.Morphology.Lemmatization.dll")
from SCICT.NLP.Morphology.Lemmatization import PersianSuffixRecognizer

class PLemmatization():
	"""docstring for PLemmatization"""
		

	def lemma(self, token):
		suffixRecognizer =  PersianSuffixRecognizer(False);
		sample1 = suffixRecognizer.MatchForSuffix(token);
		return sample1
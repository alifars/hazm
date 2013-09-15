#-*- coding: utf-8 -*-
import clr
clr.AddReference("./Virastyar.NLP.Morphology.Inflection.dll")
clr.AddReference("./Virastyar.PersianTools.dll")
clr.AddReference("./Virastyar.Utility.dll")
from Virastyar.NLP.Morphology.Inflection import PersianLemmatizer
from Virastyar.NLP.Morphology.Inflection import WordFormationInfo
import Virastyar.NLP.Morphology.Inflection.PhoneticComparison as PhoneticComparison
import Virastyar.NLP.Morphology.Inflection.StringMatching as StringMatching

class VirastyarPersianLemmatizer():
	""" 

	>>> PersianLemmatizer().lemma(u'کتباها')
	کتاب
	>>> PersianLemmatizer().lemma(u'می‌خورم')
	می‌خور
	>>> PersianLemmatizer(string_matching=False).lemma(u'کتابها')
	کتابها
	# it check PseudoSpaces
	# if string_matching == True, it ignore checking all PseudoSpaces

	>>> PersianLemmatizer(phonetic_comparison=True).lemma(u'دانام')
	دان
	>>> PersianLemmatizer(phonetic_comparison=False).lemma(u'دانام')
	دانام

	# if ignore_lexicalLemma == False, it check and search for data in 'Dic.dat' else ignore it(Rule base lemmatization)


	>>> PersianLemmatizer(ignore_declentionRules == False).lemma(u'می‌کتاب')
	می‌کتاب
	>>> PersianLemmatizer(ignore_declentionRules == True).lemma(u'می‌کتاب')
	کتاب
	
	"""

	def __init__(self, string_matching=True, phonetic_comparison=True, ignore_lexicalLemma=False, ignore_declentionRules=True):
		if string_matching == True:
			self.StringMatchingStatus = StringMatching.IgnorePseudoSpace
		else:
			self.StringMatchingStatus = StringMatching.StrictSpacing

		if phonetic_comparison == True:
			self.PhoneticComparisonStatus = PhoneticComparison.IgnorePhonetic
		else:
			self.PhoneticComparisonStatus = PhoneticComparison.StrictPhonetic

		self.ignoreLexicalLemmaStatus = ignore_lexicalLemma
		self.ignoreDeclentionRules = ignore_declentionRules
		self.suffixRecognizer =  PersianLemmatizer(False, False, "./Dic.dat")

	def lemma(self, token):
		
		lemmawords = self.suffixRecognizer.Lemmatize(token, self.StringMatchingStatus, self.PhoneticComparisonStatus, self.ignoreLexicalLemmaStatus, self.ignoreDeclentionRules)
		if len(lemmawords) == 0:
			return token
		else:
			return lemmawords[0].Lemma

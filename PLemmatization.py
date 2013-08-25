#-*- coding: utf-8 -*-
import sys
sys.path.append('/usr/lib/python2.7')
import string, clr
clr.AddReference("./Virastyar.NLP.Morphology.Inflection.dll")
clr.AddReference("./Virastyar.PersianTools.dll")
clr.AddReference("./Virastyar.Utility.dll")
from Virastyar.NLP.Morphology.Inflection import PersianLemmatizer
from Virastyar.NLP.Morphology.Inflection import WordFormationInfo
import Virastyar.NLP.Morphology.Inflection.PhoneticComparison as PhoneticComparison
import Virastyar.NLP.Morphology.Inflection.StringMatching as StringMatching

class PLemmatization():
	"""docstring for PLemmatization"""
		
	def __init__(self, string_matching = True , phonetic_comparison = True , ignore_lexicalLemma = False , ignore_declentionRules = True ):
		if string_matching == True:
			self.StringMatchingStatus = StringMatching.IgnorePseudoSpace
		else:
			self.StringMatchingStatus = StringMatching.StrictSpacing

		if phonetic_comparison == True:
			self.PhoneticComparisonStatus= PhoneticComparison.IgnorePhonetic
		else:
			self.PhoneticComparisonStatus = PhoneticComparison.StrictPhonetic

		self.ignoreLexicalLemmaStatus = ignore_lexicalLemma
		self.ignoreDeclentionRules = ignore_declentionRules
		

	def lemma(self, token):
		suffixRecognizer =  PersianLemmatizer(False , False , "./Dic.dat")
		sample1 = suffixRecognizer.Lemmatize(token , self.StringMatchingStatus , self.PhoneticComparisonStatus , self.ignoreLexicalLemmaStatus , self.ignoreDeclentionRules )
		
		'''
		# if string_matching == True, it ignore checking all PseudoSpaces
		کتاب‌ها -> کتاب
		کتابها (without PseudoSpace) -> کتاب
		but if string_matching == False, it check PseudoSpaces
		کتاب‌ها -> کتاب
		کتابها (without PseudoSpace) -> کتابها

		# if phonetic_comparison == True, it igneore checking Phonetics
		دانام -> دانا
		but if phonetic_comparison == False, it check Phonetics
		دانام -> دانام

		# if ignore_lexicalLemma == False, it check and search for data in 'Dic.dat' else ignore it(Rule base lemmatization)

		# if ignore_declentionRules == False, it check declentionRules 
		می‌کتاب -> می‌کتاب
		else it dont check declentionRules
		می‌کتاب -> کتاب
		'''
		if len(sample1) == 0 :
			return token
		else :
			return sample1[0].Lemma
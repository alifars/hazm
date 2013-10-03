from __future__ import print_function
from nltk.corpus import PlaintextCorpusReader
from pyquery import PyQuery as pq
from hazm.PersianTextNormalizer import *
from hazm.PersianTokenizer import *
import nltk, os, re, sys

class HamshahriReader():
	def __init__(self, 	hamshahri_root):
		self.hamshahri_root = hamshahri_root

	def years(self):
		"""
			Returns sorted list of year folder
			
			>>> hr.years()
			['1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007']
		"""
		return sorted(os.listdir(self.hamshahri_root))

	def fileids(self, years='*'):
		"""
			Returns list all files or files exist in specific folder(s)
			
			>>> len(hr.fileids())
			3206
			>>> len(hr.fileids(years=1996))
			157
			>>> len(hr.fileids(years=[1996,2007]))
			246
			>>> hr.fileids()[0]
			'1996/HAM2-960622.xml'
		"""
		if type(years) is int:
			years = [str(years)]
		
		if years=='*':
			wordlists = PlaintextCorpusReader(self.hamshahri_root, '.*\.xml')
			fids = wordlists.fileids()
			return fids
		else:
			fids = []
			for year in years:
				wordlists = PlaintextCorpusReader(self.hamshahri_root, str(year) + '/.*\.xml')
				fids = fids + wordlists.fileids()
			return fids

	def abspath(self, fileid):
		"""
			Returns absolute path of fileid
		"""
		return self.hamshahri_root + "/" + fileid
		
	def root(self):
		"""
			Returns root folder of Hamshahri corpus
		"""		
		return self.hamshahri_root
			
	def raw(self, fileid):
		"""
			Returns raw text of fileid
			
			>>> hr.raw('1996/HAM2-960622.xml')[:38]
			'<?xml version="1.0" encoding="UTF-8"?>'
		"""		
		wordlists = PlaintextCorpusReader(self.hamshahri_root, fileid)
		return wordlists.raw(fileid)
		
	def docs(self, years='*', fids='*'):
		"""
			Returns list of Document objects that contains information of each document in hamshahri corpus
			
			>>> list(hr.docs(fids='1996/HAM2-961221.xml'))[0].id
			'HAM2-751001-001'
			
			>>> list(hr.docs(fids='1996/HAM2-961221.xml'))[10].category
			'Science and Culture'
		"""
		if type(years) is int:
			years = [str(years)]
		
		if (fids == '*'):
			fids = self.fileids(years)
		elif type(years) is str:
			fids = [fids]

		for fid in fids:
			try:
				corpus = self.raw(fid)
				corpus = corpus.replace('<![CDATA[', '').replace(']]>', '')
				corpus = corpus.encode('utf-8')
				d = pq(corpus, parser='html')
				for doc in d('DOC'):
					dc = pq(doc)
					document = Document()
					document.id = dc('DOCID').text()
					document.number = dc('DOCNO').text()
					document.originalfile = dc('ORIGINALFILE').text()
					document.issue = dc('ISSUE').text()
					document.date = dc('DATE[calender=Western]').text()
					document.persiandate = dc('DATE[calender=Persian]').text()
					document.category = dc('CAT[xml\:lang=en]').text()
					document.persiancategory = dc('CAT[xml\:lang=fa]').text()
					document.title = dc('TITLE').text()
					document.text = dc('TEXT').text()
					yield  document
			except:
				print('Format of "' + fid + '" file is not appropriate', file=sys.stderr)
			
	def categories(self, years='*', fids='*', lang='en'):
		"""
			Returns list of categories
		
			>>> len(hr.categories(fids='1996/HAM2-961221.xml'))
			10
			
			>>> len(hr.categories(fids=['1996/HAM2-961221.xml','2007/HAM2-070101.xml']))
			17
			
			>>> len(hr.categories(years=2005))
			24
			
			>>> len(hr.categories(fids='1996/HAM2-961221.xml',lang='fa'))
			10
		"""
		if type(years) is int:
			years = [str(years)]
		
		if (fids == '*'):
			fids = self.fileids(years)
		elif type(years) is str:
			fids = [fids]
			
		categories = set()
		for fid in fids:
			try:
				corpus = self.raw(fid)
				corpus = corpus.replace('<![CDATA[', '').replace(']]>', '')
				corpus = corpus.encode('utf-8')

				d = pq(corpus, parser='html')
				for cat in d('CAT[xml\:lang=' + lang + ']'):
					categories.add(pq(cat).text())
			except:
				print('Format of "' + fid + '" file is not appropriate', file=sys.stderr)
		return list(categories)

	def texts(self, years='*', fids='*', normalize=True):
		"""
			Returns list of sentences
		
			>>> len(list(hr.texts(fids='1996/HAM2-961221.xml'))[0])
			2243
		"""
		if type(years) is int:
			years = [str(years)]
		
		if (fids == '*'):
			fids = self.fileids(years)
		elif type(years) is str:
			fids = [fids]

		normalizer = PersianTextNormalizer()
			
		for fid in fids:
			try:
				corpus = self.raw(fid)
				corpus = corpus.replace('<![CDATA[', '').replace(']]>', '')
				corpus = corpus.encode('utf-8')
				d = pq(corpus, parser='html')
				for cat in d('TEXT'):
					data = pq(cat)
					data.remove('image')
					text = data.text()
					if (normalize == True):
						text = normalizer.cleanup(text)
					yield text
			except:
				print('Format of "' + fid + '" file is not appropriate', file=sys.stderr)
		
	def sents(self, years='*', fids='*', normalize=True):
		"""
			Returns list of sentences
		
			>>> len(list(hr.sents(fids='1996/HAM2-961221.xml'))[0])
			173
		"""
		tokenizer = PersianTokenizer()
		for text in self.texts(years, fids, normalize):
			for sent in tokenizer.sent_tokenize(text):
				yield sent

		
	def words(self, years='*', fids='*', normalize=True):
		"""
			Returns a list contains list of words in each sentence
		
			>>> len(list(hr.words(fids='1996/HAM2-961221.xml'))[0])
			39
		"""
		tokenizer = PersianTokenizer()
		for sent in self.sents(years, fids, normalize):
			yield tokenizer.word_tokenize(sent)

class Document:
	id = ''
	number = ''
	originalfile= ''
	issue= ''
	date= ''
	persiandate= ''
	category= ''
	persiancategory= ''
	title= ''
	text= ''

if __name__ == "__main__":
    import doctest
    doctest.testmod(extraglobs={'hr': HamshahriReader('/home/server/hazm/data/hamshahri')})
    

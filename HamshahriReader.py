from nltk.corpus import PlaintextCorpusReader
from pyquery import PyQuery as pq
import nltk, os, re

hamshahri_root = '/home/server/pltk/data/hamshahri'

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


def years():
	"""
		Returns sorted list of year folder
		
		>>> years()
		['1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007']
	"""
	return sorted(os.listdir(hamshahri_root))

def fileids(years='*'):
	"""
		Returns list all files or files exist in specific folder(s)
		
		>>> len(fileids())
		3206
		>>> len(fileids(years=1996))
		157
		>>> len(fileids(years=[1996,2007]))
		246
		>>> fileids()[0]
		'1996/HAM2-960622.xml'
	"""
	if type(years) is int:
		years = [str(years)]
	
	if years=='*':
		wordlists = PlaintextCorpusReader(hamshahri_root, '.*\.xml')
		fids = wordlists.fileids()
		return fids
	else:
		fids = []
		for year in years:
			wordlists = PlaintextCorpusReader(hamshahri_root, str(year) + '/.*\.xml')
			fids = fids + wordlists.fileids()
		return fids

def abspath(fileid):
	"""
		Returns absolute path of fileid
		
		>>> abspath('1996/HAM2-960622.xml')
		'/home/server/corpora/hamshahri/1996/HAM2-960622.xml'
	"""
	return hamshahri_root + "/" + fileid
	
def root():
	"""
		Returns root folder of Hamshahri corpus
		
		>>> root()
		'/home/server/corpora/hamshahri'
	"""		
	return hamshahri_root
		
def raw(fileid):
	"""
		Returns raw text of fileid
		
		>>> raw('1996/HAM2-960622.xml')[:38]
		'<?xml version="1.0" encoding="UTF-8"?>'
	"""		
	wordlists = PlaintextCorpusReader(hamshahri_root, fileid)
	return wordlists.raw(fileid)
	
def docs(years='*', fids='*'):
	"""
		Returns list of Document objects that contains information of each document in hamshahri corpus
		
		>>> list(docs(fids='1996/HAM2-961221.xml'))[0].id
		'HAM2-751001-001'
		
		>>> list(docs(fids='1996/HAM2-961221.xml'))[10].category
		'Science and Culture'
	"""
	if type(years) is int:
		years = [str(years)]
	
	if (fids == '*'):
		fids = fileids(years)
	elif type(years) is str:
		fids = [fids]

	for fid in fids:
		corpus = raw(fid)
		corpus = corpus.replace('<![CDATA[', '').replace(']]>', '')
		try:
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
			print('Format of "' + fid + '" file is not appropriate')
		
def categories(years='*', fids='*', lang='en'):
	"""
		Returns list of categories
	
		>>> len(categories(fids='1996/HAM2-961221.xml'))
		10
		
		>>> len(categories(fids=['1996/HAM2-961221.xml','2007/HAM2-070101.xml']))
		17
		
		>>> len(categories(years=2005))
		24
		
		>>> len(categories(fids='1996/HAM2-961221.xml',lang='fa'))
		10
	"""
	if type(years) is int:
		years = [str(years)]
	
	if (fids == '*'):
		fids = fileids(years)
	elif type(years) is str:
		fids = [fids]
		
	categories = set()
	for fid in fids:
		corpus = raw(fid)
		corpus = corpus.replace('<![CDATA[', '').replace(']]>', '')
		try:
			d = pq(corpus, parser='html')
			for cat in d('CAT[xml\:lang=' + lang + ']'):
				categories.add(pq(cat).text())
		except:
			print('Format of "' + fid + '" file is not appropriate')
	return list(categories)
	
def sents(years='*', fids='*'):
	"""
		Returns list of sentences
	
		>>> len(list(sents(fids='1996/HAM2-961221.xml'))[0])
		2436
	"""
	if type(years) is int:
		years = [str(years)]
	
	if (fids == '*'):
		fids = fileids(years)
	elif type(years) is str:
		fids = [fids]
		
	for fid in fids:
		corpus = raw(fid)
		corpus = corpus.replace('<![CDATA[', '').replace(']]>', '')
		try:
			d = pq(corpus, parser='html')
			for cat in d('TEXT'):
				data = pq(cat).html()
				pattern = re.compile(r'<image>.*?</image>')
				data = pattern.sub('', data)
				text = nltk.clean_html(data)
				yield text
		except:
			print('Format of "' + fid + '" file is not appropriate')

	
	#words()
from nltk.tag.stanford import POSTagger
from nltk.tag import str2tuple
import subprocess

class PersianPOSTagger(POSTagger):
	"""
		An interface to pos tagging with Stanford Tagger on the bijankhan corpus.
		 - a model trained on training data
		 - (optionally) the path to the stanford tagger jar file. If not specified here,
       then this jar file must be specified in the CLASSPATH envinroment variable.
         - (optionally) the encoding of the training data (default: UTF8)
	"""

	_SEPARATOR = '/'
	_path_to_jar = '/home/server/pltk/resources/stanford-postagger.jar'
	bijankhan_path = '/home/server/pltk/data/bijankhan.txt'

	def __init__(self, *args, **kwargs):
		lst = list(args)
		args_count = len(args)
		if (args_count >= 2):
			lst[1] = self._path_to_jar
		else:
			kwargs['path_to_jar'] = self._path_to_jar

		if (args_count >= 3):
			lst[2] = 'utf8'
		else:
			kwargs['encoding'] = 'utf8'
		args = tuple(lst)

		super(PersianPOSTagger, self).__init__(*args, **kwargs)		

	@staticmethod
	def train(train_file, properties, model, xms='-Xms1g', xmx='-Xmx2g', verbose=True):
		"""
			>>> PersianPOSTagger.train('/home/server/pltk/data/bijankhan-train.txt','/home/server/pltk/data/persian-left3words-distsim.tagger.props', '/home/server/pltk/data/persian.mco')
		"""
		#	def train(self, train_file, properties, model, xms='-Xms120m', xmx='-Xmx1g'):
		#		cmd = ['java', xms, xmx, '-classpath', self._path_to_jar, 'edu.stanford.nlp.tagger.maxent.MaxentTagger',
		path_to_jar = '/home/server/pltk/resources/stanford-postagger.jar'
		cmd = ['java', xms, xmx, '-classpath', path_to_jar, 'edu.stanford.nlp.tagger.maxent.MaxentTagger',
                   '-prop', properties,
                   '-model', model, 
                   '-trainFile', train_file,
                   '-tagSeparator', '/']
		output=subprocess.PIPE
		if (verbose == True):
			p = subprocess.Popen(cmd)
		else:
			p = subprocess.Popen(cmd, stdout=output, stderr=output)

	def evaluate_file(self, gold_file):
		corpus = []
		tag_convert = lambda t: (t[0].decode('utf-8'), t[1].decode('utf-8'))
		lines = open(gold_file).readlines()
		for sent in lines:
			corpus.append([tag_convert(str2tuple(t)) for t in sent.split()])
		return super(PersianPOSTagger, self).evaluate(corpus)

if __name__ == '__main__':
	PersianPOSTagger.train('/home/server/pltk/data/bijankhan-train.txt','/home/server/pltk/data/persian-left3words-distsim.tagger.props', '/home/server/pltk/data/persian.tagger')
	st = PersianPOSTagger('/home/server/pltk/data/persian.tagger')
	st.evaluate_file('/home/server/pltk/data/bijankhan-test.txt')
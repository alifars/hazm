from nltk.parse.malt import MaltParser
from PersianPOSTagger import *
from nltk.data import ZipFilePathPointer
from PersianTokenizer import *
from PersianTextNormalizer import *
import os

class PersianDependencyParser(MaltParser):

	def __init__(self, tagger=None, mco=None, working_dir="data/parse", path_to_malt="resources"):
		os.environ["MALTPARSERHOME"] = path_to_malt
		self._tokenizer = PersianTokenizer()
		self._normalizer = PersianTextNormalizer()
		#if tagger is None:
		#	tagger = PersianPOSTagger('data/persian.tagger')
		super(PersianDependencyParser, self).__init__(tagger, mco, working_dir)

	def raw_parse(self, sentence, verbose=False):
		"""
		Use MaltParser to parse a sentence. Takes a sentence as a string;
		before parsing, it will be automatically tokenized and tagged with this
		MaltParser instance's tagger.

		:param sentence: Input sentence to parse
		:type sentence: str
		:return: ``DependencyGraph`` the dependency graph representation of the sentence
		"""
		sentence = self._normalizer.cleanup(sentence)
		for sent in self._tokenizer.sent_tokenize(sentence):
			words = self._tokenizer.word_tokenize(sent)
			return self.parse(words, verbose)

	def train_from_file(self, conll_file, option_file, guide_file, xms='-Xms1g', xmx='-Xmx2g', verbose=False):
		"""
		Train MaltParser from a file

		:param conll_file: str for the filename of the training input data
		:param option_file: str for the filename of the option file
		:param guide_file: str for the filename of the guide file for specifying the feature model specification file
		"""
		if not self._malt_bin:
			raise Exception("MaltParser location is not configured. Call config_malt() first.")

		# If conll_file is a ZipFilePathPointer, then we need to do some extra
		# massaging
		if isinstance(conll_file, ZipFilePathPointer):
			input_file = tempfile.NamedTemporaryFile(prefix='malt_train.conll',
													 dir=self.working_dir,
													 delete=False)
			try:
				conll_str = conll_file.open().read()
				conll_file.close()
				input_file.write(conll_str)
				input_file.close()
				return self.train_from_file(input_file.name, verbose=verbose)
			finally:
				input_file.close()
				os.remove(input_file.name)

		cmd = ['java', xms, xmx, '-jar', self._malt_bin, '-w', self.working_dir,
			   '-c', self.mco, '-i', conll_file, '-f', option_file,
			   '-F', guide_file, '-m', 'learn']

		ret = self._execute(cmd, verbose)
		if ret != 0:
			raise Exception("MaltParser training (%s) "
							"failed with exit code %d" %
							(' '.join(cmd), ret))

		self._trained = True

if __name__ == '__main__':
	parser = PersianDependencyParser(mco="persian")
	parser.train_from_file('data/train.conll', 'data/parse/optionsFile.xml', 'data/parse/guideFile.xml', verbose=True)
	txt = "This is a test sentence"
	graph = parser.raw_parse(txt)
	graph.tree().pprint()
from nltk.parse.malt import MaltParser
from operator import add
from nltk.internals import find_binary
import glob

class PersianDependencyParser(MaltParser):

	def __init__(self, tagger=None, mco=None, working_dir=None):
		super(PersianDependencyParser, self).__init__(tagger, mco, working_dir)

#if __name__ == '__main__':
#	parser = PersianDependencyParser()
#	parser.parse()
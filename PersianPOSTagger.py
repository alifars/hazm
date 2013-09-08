from nltk.tag.stanford import POSTagger
import re

bijankhan_path = '/home/server/pltk/data/bijankhan.txt'

class PersianPOSTagger(POSTagger):
	"""
		An interface to pos tagging with Stanford Tagger on the bijankhan corpus.
		 - a model trained on training data
		 - (optionally) the path to the stanford tagger jar file. If not specified here,
       then this jar file must be specified in the CLASSPATH envinroment variable.
         - (optionally) the encoding of the training data (default: UTF8)
	"""

	def __init__(self, *args, **kwargs):
		args['encoding'] = 'utf8'
		if 'jar' not in args:
			args['jar'] = '/home/server/pltk/resources/stanford-postagger.jar'
        super(PersianPOSTagger, self).__init__(*args, **kwargs)

	def convert_to_stanford_format(input, output, hasGold=True):
		writer = open(output, 'w')
		lines = open(input).readlines()
		newLine = True
		for line in lines:
			line = line.strip('\r\n')
			words = re.split(" +", line)

			if (words[0] == '#'):
				newLine = True
				writer.write("\n")
			else:
				if (newLine == False):
					writer.write(" ")
				writer.write(words[0])
				if (hasGold == True):
					writer.write("/" + words[1])
				newLine = False
				if (words[0] == '.' and words[1] == 'DELM'):
					newLine = True
					writer.write("\n")



		


#PersianPOSTagger(jar='')
#		self._JAR
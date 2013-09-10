from nltk.tag.stanford import POSTagger
import re, subprocess

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

	def convert_to_stanford_format(self, input, output, hasGold=True):
		writer = open(output, 'w')
		lines = open(input).readlines()
		newLine = True
		for line in lines:
			line = line.strip('\r\n')
			words = re.split(" +", line)

			if (words[0] == '#'):
				if (newLine == False):
					writer.write("\n")
				newLine = True
			else:
				if (newLine == False):
					writer.write(" ")
				writer.write("_".join(words[0:len(words)-1]))
				if (hasGold == True):
					writer.write("/" + words[len(words)-1])
				newLine = False
				if (words[0] == '.' and words[len(words)-1] == 'DELM'):
					newLine = True
					writer.write("\n")

	def train(self, train_file, properties, model, xms='-Xms120m', xmx='-Xmx1g'):
		cmd = ['java', xms, xmx, '-classpath', self._path_to_jar, 'edu.stanford.nlp.tagger.maxent.MaxentTagger',
                   '-prop', properties,
                   '-model', model, 
                   '-trainFile', train_file,
                   '-tagSeparator', '/']
		output=subprocess.PIPE
		p = subprocess.Popen(cmd, stdout=output, stderr=output)
		

#PersianPOSTagger(jar='')
#		self._JAR
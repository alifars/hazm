import re

class PersianTextNormalizer():
	# The PersianTextNormalizer class contains a python version of the original 
	# ruby implementation of virastar (https://github.com/aziz/virastar) and
	# Persian Pre-processor (PrePer) described in:
	# 	- 	Seraji Mojgan, Beáta Megyesi, Joakim Nivre. 2012. 
	#		A Basic Language Resource Kit for Persian. 
	#		In Proceedings of the 8th International Conference on Language Resources and Evaluation (LREC). 
	#		Istanbul, Turkey.

	def __init__(self, 	fix_dashes=True,
						fix_three_dots=True,
						fix_english_quotes=True
						fix_hamzeh=True
						cleanup_zwnj=True
						fix_english_numbers=True
						fix_arabic_numbers=True
						fix_misc_non_persian_chars=True
						fix_perfix_spacing=True
						fix_suffix_spacing=True
						aggresive=True
						cleanup_extra_marks=True
						cleanup_kashidas=True
						fix_spacing_for_braces_and_quotes=True
						cleanup_spacing=True
						cleanup_begin_and_end=True):
		self._fix_dashes = fix_dashes
		self._fix_three_dots = fix_three_dots
		self._fix_english_quotes = fix_english_quotes
		self._fix_hamzeh = fix_hamzeh
		self._cleanup_zwnj = cleanup_zwnj
		self._fix_english_numbers = fix_english_numbers
		self._fix_arabic_numbers = fix_arabic_numbers
		self._fix_misc_non_persian_chars = fix_misc_non_persian_chars
		self._fix_perfix_spacing = fix_perfix_spacing
		self._fix_suffix_spacing = fix_suffix_spacing
		self._aggresive = aggresive
		self._cleanup_extra_marks = cleanup_extra_marks
		self._cleanup_kashidas = cleanup_kashidas
		self._fix_spacing_for_braces_and_quotes = fix_spacing_for_braces_and_quotes
		self._cleanup_spacing = cleanup_spacing
		self._cleanup_begin_and_end = cleanup_begin_and_end

	def cleanup(self, text):
		# removing URLS bringing them back at the end of process
		urls = []
		pattern = r'https?:\/\/([-\w\.]+)+(:\d+)?(\/([\w\/_\.]*(\?\S+)?)?)?'
		iterator = finditer(pattern, text)
		i = 0
		for match in iterator:
			urls.append(match.group(0))
			text = text.replace(match.group(0), "__urls__" + str(i) + "__", 1)
			i = i + 1

		if (self._fix_dashes):
			text = self.fix_dashes(fix_dashes)
		if (self._fix_three_dots):
			text = self.fix_three_dots(text)
		if (self._fix_english_quotes):
			text = self.fix_english_quotes(text)
		if (self._fix_hamzeh):
			text = self.fix_hamzeh(text)
		if (self._cleanup_zwnj):
			text = self.cleanup_zwnj(text)
		if (self._fix_english_numbers):
			text = self.fix_english_numbers(text)
		if (self._fix_arabic_numbers):
			text = self.fix_arabic_numbers(text)
		if (self._fix_misc_non_persian_chars):
			text = self.fix_misc_non_persian_chars(text)
		if (self._fix_perfix_spacing):
			text = self.fix_perfix_spacing(text)
		if (self._fix_suffix_spacing):
			text = self.fix_suffix_spacing(text)
		# Aggressive Editing
		if (self._aggresive):
			if (self._cleanup_extra_marks):
				text = self.cleanup_extra_marks(text)
			if (self._cleanup_kashidas):
				text = self.cleanup_kashidas(text)
		if (self._fix_spacing_for_braces_and_quotes):
			text = self.fix_spacing_for_braces_and_quotes(text)
		if (self._cleanup_spacing):
			text = self.cleanup_spacing(text)
		if (self._cleanup_begin_and_end):
			text = self.cleanup_begin_and_end(text)

		# bringing back urls
		pattern = r'__urls__\d+__'
		iterator = finditer(pattern, text)
		for match in iterator:
			parts = match.group(0).split("__")
			index = int(parts[len(parts)-2])
			text = text.replace(match.group(0), urls[index], 1)

		return text

	persian_numbers = "۱۲۳۴۵۶۷۸۹۰"
	arabic_numbers  = "١٢٣٤٥٦٧٨٩٠"
	english_numbers = "1234567890"
	bad_chars  = ",;كي%"
	good_chars = "،؛کی٪"

	def fix_dashes(self, text):
		"""
			replace double dash to ndash and triple dash to mdash

			>>> fix_dashes('صفحه 2--4')
			'صفحه 2–4'
		"""
		pattern = re.compile('-{3}', flags=re.DOTALL)
		text = pattern.sub('—', text)

		pattern = re.compile('-{2}', flags=re.DOTALL)
		text = pattern.sub('–', text)

		return text

	def fix_three_dots(self, text):
		"""
			replace three dots with ellipsis

			>>> fix_three_dots('1, 2, 3, ..., 10')
			'1, 2, 3,…, 10'
		"""
		pattern = re.compile(r'\s*\.{3,}', flags=re.DOTALL)
		return pattern.sub('…', text)

	def fix_english_quotes(self, text):
		"""
			replace English quotes with their Persian equivalent
		"""
		pattern = re.compile(r'(["\'`]+)(.+?)(\1)', flags=re.DOTALL)
		return pattern.sub(r'«\2»', text)

	def fix_hamzeh(self, text):
		"""
			should convert ه ی to ه
		"""
		# \s	any whitespace (space, tab, line break)
		# \S	any character except whitespace
		pattern = re.compile(r'(\S)(ه[\s\u200c‌]+[یي])(\s)', flags=re.DOTALL)
		return pattern.sub(r'\1هٔ\3', text)

	def cleanup_zwnj(self, text):
		"""
			remove unnecessary zwnj char that are succeeded/preceded by a space
		"""
		pattern = re.compile(r'\s+‌|‌\s+', flags=re.DOTALL)
		return pattern.sub(' ', text)

	def fix_spacing_for_braces_and_quotes(self, text):
		# should fix outside and inside spacing for () [] {}  “” «»
		pattern = re.compile(r'[ \t‌]*(\()\s*([^)]+?)\s*?(\))[ \t‌]*', flags=re.DOTALL)
		text = pattern.sub(r' \1\2\3 ', text)

		pattern = re.compile(r'[ \t‌]*(\[)\s*([^\]]+?)\s*?(\])[ \t‌]*', flags=re.DOTALL)
		text = pattern.sub(r' \1\2\3 ', text)

		pattern = re.compile(r'[ \t‌]*(\{)\s*([^}]+?)\s*?(\})[ \t‌]*', flags=re.DOTALL)
		text = pattern.sub(r' \1\2\3 ', text)

		pattern = re.compile(r'[ \t‌]*(“)\s*([^”]+?)\s*?(”)[ \t‌]*', flags=re.DOTALL)
		text = pattern.sub(r' \1\2\3 ', text)

		pattern = re.compile(r'[ \t‌]*(«)\s*([^»]+?)\s*?(»)[ \t‌]*', flags=re.DOTALL)
		text = pattern.sub(r' \1\2\3 ', text)

		# : ; , . ! ? and their persian equivalents should have one space after and no space before
		pattern = re.compile(r'[ \t‌]*([:;,؛،.؟!]{1})[ \t‌]*', flags=re.DOTALL)
		text = pattern.sub(r'\1 ', text)

        # do not put space after colon that separates time parts
		pattern = re.compile(r'([۰-۹]+):\s+([۰-۹]+)', flags=re.DOTALL)
		text = pattern.sub(r'\1:\2', text)

	  	# should fix inside spacing for () [] {}  “” «»
		pattern = re.compile(r'(\()\s*([^)]+?)\s*?(\))', flags=re.DOTALL)
		text = pattern.sub(r'\1\2\3', text)

		pattern = re.compile(r'(\[)\s*([^\]]+?)\s*?(\])', flags=re.DOTALL)
		text = pattern.sub(r'\1\2\3', text)
		
		pattern = re.compile(r'(\{)\s*([^}]+?)\s*?(\})', flags=re.DOTALL)
		text = pattern.sub(r'\1\2\3', text)
		
		pattern = re.compile(r'(“)\s*([^”]+?)\s*?(”)', flags=re.DOTALL)
		text = pattern.sub(r'\1\2\3', text)

		pattern = re.compile(r'(«)\s*([^»]+?)\s*?(»)', flags=re.DOTALL)
		text = pattern.sub(r'\1\2\3', text)

		return text

	def fix_english_numbers(self, text):
		"""
			>>> fix_english_numbers('1234-۱۲۳۴-١٢٣٤')
			'۱۲۳۴-۱۲۳۴-١٢٣٤'
		"""
		text = text.translate(str.maketrans(self.english_numbers, self.persian_numbers))

		# should not replace exnglish chars in english phrases
		pattern = r'([a-zA-Z\-_]{2,}[۰-۹]+|[۰-۹]+[a-zA-Z\-_]{2,})'
		iterator = finditer(pattern, text, flags=re.IGNORECASE)
		for match in iterator:
			new_text = match.group(0).translate(str.maketrans(self.persian_numbers, self.english_numbers))
			text.replace(match.group(0), new_text, 1)

		return text

	def fix_arabic_numbers(self, text):
		"""
			>>> fix_arabic_numbers('1234-۱۲۳۴-١٢٣٤')
			'1234-۱۲۳۴-۱۲۳۴'
		"""
		return text.translate(str.maketrans(self.arabic_numbers, self.persian_numbers))
		# python 2
		#	from string import maketrans
		#	return text.translate(maketrans(self.arabic_numbers, self.persian_numbers))

	def fix_misc_non_persian_chars(self, text):
		"""
			>>> fix_misc_non_persian_chars('علي')
			'علی'
		"""
		return text.translate(str.maketrans(self.bad_chars, self.good_chars))

	def fix_perfix_spacing(self, text):
		"""
			put zwnj between word and prefix (mi* nemi*)
			there's a possible bug here: می and نمی could be separate nouns and not prefix
		"""
		pattern = re.compile(r'\s+(ن?می)\s+', flags=re.DOTALL)
		return pattern.sub(r' \1‌', text)

	def fix_suffix_spacing(self, text):
		"""
			put zwnj between word and suffix (*tar *tarin *ha *haye)
			there's a possible bug here: های and تر could be separate nouns and not suffix
		"""
		# in case you can not read it: \s+(tar(i(n)?)?|ha(ye)?)\s+
		pattern = re.compile(r'\s+(تر(ی(ن)?)?|ها(ی)?)\s+', flags=re.DOTALL)
		return pattern.sub(r'‌\1 ', text)

	def cleanup_extra_marks(self, text):
		"""
			replace more than one ! or ? mark with just one

			>>> cleanup_extra_marks('نه!!!!!')
			'نه!'
		"""
		pattern = re.compile(r'(!){2,}', flags=re.DOTALL)
		text = pattern.sub(r'\1', text)

		pattern = re.compile(r'(؟){2,}', flags=re.DOTALL)
		text = pattern.sub(r'\1', text)

		return text

	def cleanup_kashidas(self, text):
		"""
			should remove all kashida (کشیده)

			>>> cleanup_kashidas('رحــــــيم')
			'رحيم'
		"""
		pattern = re.compile(r'ـ+', flags=re.DOTALL)
		return pattern.sub('', text)

	def cleanup_spacing(self, text):
		"""
			should replace more than one space with just a single one
		"""
		pattern = re.compile(r'[ ]+', flags=re.DOTALL)
		text = pattern.sub(' ', text)

		pattern = re.compile(r'([\n]+)[ \t‌]*', flags=re.DOTALL)
		text = pattern.sub(r'\1', text)

		return text

	def cleanup_begin_and_end(self, text):
		"""
			remove spaces, tabs, and new lines from the beginning and enf of file
		"""
		return text.strip()
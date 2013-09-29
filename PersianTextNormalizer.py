import re

class PersianTextNormalizer():
	# The PersianTextNormalizer class contains a python version of the original 
	# ruby implementation of virastar v0.0.6 (https://github.com/aziz/virastar) and
	# Persian Pre-processor (PrePer) described in:
	# 	- 	Seraji Mojgan, Beáta Megyesi, Joakim Nivre. 2012. 
	#		A Basic Language Resource Kit for Persian. 
	#		In Proceedings of the 8th International Conference on Language Resources and Evaluation (LREC). 
	#		Istanbul, Turkey.

	def __init__(self, 	fix_dashes=True,
						fix_three_dots=True,
						fix_english_quotes=True,
						fix_hamzeh=True,
						cleanup_zwnj=True,
						fix_english_numbers=True,
						fix_arabic_numbers=True,
						fix_misc_non_persian_chars=True,
						fix_perfix_spacing=True,
						fix_suffix_spacing=True,
						aggresive=True,
						cleanup_extra_marks=True,
						cleanup_kashidas=True,
						fix_spacing_for_braces_and_quotes=True,
						cleanup_spacing=True,
						cleanup_begin_and_end=True,
						fix_suffix=True,
						fix_prefix=True):
		self._fix_dashes = fix_dashes
		self._fix_dashes_pattern = [
			( re.compile('-{3}', flags=re.DOTALL), '—' ),
			( re.compile('-{2}', flags=re.DOTALL), '–' )
		]

		self._fix_three_dots = fix_three_dots
		self._fix_three_dots_pattern = re.compile(r'\s*\.{3,}', flags=re.DOTALL)

		self._fix_english_quotes = fix_english_quotes
		self._fix_english_quotes_ppattern = re.compile(r'(["\'`]+)(.+?)(\1)', flags=re.DOTALL)

		self._fix_hamzeh = fix_hamzeh
		self._fix_hamzeh_pattern = re.compile(r'(\S)(ه[\s\u200c‌]+[یي])(\s)', flags=re.DOTALL)

		self._cleanup_zwnj = cleanup_zwnj
		self._cleanup_zwnj_pattern = re.compile(r'\s+‌|‌\s+', flags=re.DOTALL)

		self._fix_english_numbers = fix_english_numbers
		self._fix_arabic_numbers = fix_arabic_numbers
		self._fix_misc_non_persian_chars = fix_misc_non_persian_chars
		self._fix_perfix_spacing = fix_perfix_spacing
		self._fix_perfix_spacing_pattern = re.compile(r'\s+(ن?می)\s+', flags=re.DOTALL)

		self._fix_suffix_spacing = fix_suffix_spacing
		# in case you can not read it: \s+(tar(i(n)?)?|ha(ye)?)\s+
		self._fix_suffix_spacing_pattern = re.compile(r'\s+(تر(ی(ن)?)?|ها(ی)?)\s+', flags=re.DOTALL)

		self._aggresive = aggresive
		self._cleanup_extra_marks = cleanup_extra_marks
		self._cleanup_extra_marks_pattern = [
			re.compile(r'(!){2,}', flags=re.DOTALL),
			re.compile(r'(؟){2,}', flags=re.DOTALL)
		]

		self._cleanup_kashidas = cleanup_kashidas
		self._cleanup_kashidas_pattern = re.compile(r'ـ+', flags=re.DOTALL)

		self._fix_spacing_for_braces_and_quotes = fix_spacing_for_braces_and_quotes
		self._fix_spacing_for_braces_and_quotes_pattern = [
			# should fix outside and inside spacing for () [] {}  “” «»
			(
				re.compile(r'[ \t‌]*(\()\s*([^)]+?)\s*?(\))[ \t‌]*', flags=re.DOTALL),
				r' \1\2\3 '
			),
			(
				re.compile(r'[ \t‌]*(\[)\s*([^\]]+?)\s*?(\])[ \t‌]*', flags=re.DOTALL),
				r' \1\2\3 '
			),
			(
				re.compile(r'[ \t‌]*(\{)\s*([^}]+?)\s*?(\})[ \t‌]*', flags=re.DOTALL),
				r' \1\2\3 '
			),
			(
				re.compile(r'[ \t‌]*(“)\s*([^”]+?)\s*?(”)[ \t‌]*', flags=re.DOTALL),
				r' \1\2\3 '
			),
			(
				re.compile(r'[ \t‌]*(«)\s*([^»]+?)\s*?(»)[ \t‌]*', flags=re.DOTALL),
				r' \1\2\3 '
			),

			# : ; , . ! ? and their persian equivalents should have one space after and no space before
			(
				re.compile(r'[ \t‌]*([:;,؛،.؟!]{1})[ \t‌]*', flags=re.DOTALL),
				r'\1 '
			),

			# do not put space after colon that separates time parts
			(
				re.compile(r'([۰-۹]+):\s+([۰-۹]+)', flags=re.DOTALL),
				r'\1:\2'
			),

			# should fix inside spacing for () [] {}  “” «»
			(
				re.compile(r'(\()\s*([^)]+?)\s*?(\))', flags=re.DOTALL),
				r'\1\2\3'
			),
			(
				re.compile(r'(\[)\s*([^\]]+?)\s*?(\])', flags=re.DOTALL),
				r'\1\2\3'
			),
			(
				re.compile(r'(\{)\s*([^}]+?)\s*?(\})', flags=re.DOTALL),
				r'\1\2\3'
			),
			(
				re.compile(r'(“)\s*([^”]+?)\s*?(”)', flags=re.DOTALL),
				r'\1\2\3'
			),
			(
				re.compile(r'(«)\s*([^»]+?)\s*?(»)', flags=re.DOTALL),
				r'\1\2\3'
			)
		]

		self._cleanup_spacing = cleanup_spacing
		self._cleanup_spacing_pattern = [
			( re.compile(r'[ ]+', flags=re.DOTALL), ' ' ),
			( re.compile(r'([\n]+)[ \t‌]*', flags=re.DOTALL), r'\1' )
		]

		self._cleanup_begin_and_end = cleanup_begin_and_end
		self._fix_suffix = fix_suffix
		self._fix_suffix_pattern = [
			( re.compile(r'\s+(((زا(ی)?)?|ام?|ات|اش|ای?(د)?|ایم?|اند?)[\.\!\?\،]*)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(های)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(هاای)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(ایی)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(ای)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(ی)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(یی)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(م|ت|ش|مان|تان|شان)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(هایی|هایم|هایت|هایش|هایمان|هایتان|هایشان)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(م|ی|د|یم|ید|ند)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(ان)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(ین)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(ات)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(جات)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(آور)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(نشین)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'(\s+)(ابداع)\s+(کننده)(\s+)', flags=re.DOTALL), r'‌\1\2‌\3\4' ),
			( re.compile(r'(\s+)(ابر)\s+(اتم)(\s+)', flags=re.DOTALL), r'‌\1\2‌\3\4' ),
			( re.compile(r'\s+(پاش(ی)?)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(پوش(ان)?)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(شناس(ی)?)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'([\n]+)[ \t‌]*', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(پذیر(ی)?)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(اندود)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(فشان(ی|ها(ی)?))\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'(\s+)(آبله)\s+(مرغان)(\s+)', flags=re.DOTALL), r'‌\1\2‌\3\4' ),
			( re.compile(r'\s+(سازی)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(آلود(ی)?)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(آمیز(ی)?)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(زدا(ی(ی)?)?)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(انگیز(ی)?)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(خیز(ی)?)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(پور)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'(\s+)(آزاد)\s+(راه)(\s+)', flags=re.DOTALL), r'‌\1\2‌\3\4' ),
			( re.compile(r'(\s+)(راه)\s+(آهن)(\s+)', flags=re.DOTALL), r'‌\1\2‌\3\4' ),
			( re.compile(r'(\s+)(راه)\s+(حل)(\s+)', flags=re.DOTALL), r'‌\1\2‌\3\4' ),
			( re.compile(r'(\s+)(راه)\s+(حلی)(\s+)', flags=re.DOTALL), r'‌\1\2‌\3\4' ),
			( re.compile(r'(\s+)(راه)\s+(اندازی)(\s+)', flags=re.DOTALL), r'‌\1\2‌\3\4' ),
			( re.compile(r'\s+(سوزی(ها(ی)?)?)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(پراکنی)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'(\s+)(اثنی)\s+(عشر)(\s+)', flags=re.DOTALL), r'‌\1\2‌\3\4' ),
			( re.compile(r'(\s+)(اثنی)\s+(عشری)(\s+)', flags=re.DOTALL), r'‌\1\2‌\3\4' ),
			( re.compile(r'\s+(خوری)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(گویان)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'(\s+)(دوان)\s+(دوان)(\s+)', flags=re.DOTALL), r'‌\1\2‌\3\4' ),
			( re.compile(r'\s+(افکنی)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(دان(ان)?)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(پرور(ی)?)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(پریش(ی)?)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(نویس(ی(ی)?)?)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(ربایان)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(کشان(ی)?)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'(\s+)(کشان)\s+(کشان)(\s+)', flags=re.DOTALL), r'‌\1\2‌\3\4' ),
			( re.compile(r'(\s+)(الدرم)\s+(بلدرم)(\s+)', flags=re.DOTALL), r'‌\1\2‌\3\4' ),
			( re.compile(r'\s+(وار(ه)?)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(مداران)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(ساله)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(پاشیدگی)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(شناسان)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(وند)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(کاران(ه)?)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(پژوه(ی)?)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(زا(یی|ای)?)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'([\n]+)[ \t‌]*', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(ریزان)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(کنندگی)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(زاد)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(سنج(ی)?)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(کنان)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(پرداز(ی)?)\s+', flags=re.DOTALL), r'‌\1 '),
			( re.compile(r'\s+(رسانی)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(زی)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(وار(ه)?)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(یاب(ی)?)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(گان(ه)?)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(پیما(ها(ی(ی)?)?)?)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(گی)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(گر(ی)?)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(یت)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(کان)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(اک)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(ناک)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(ک)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(انه)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(ه)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(مند)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(ور)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(گین)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(سار)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(ساعته)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(اً)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(ار)\s+', flags=re.DOTALL), r'‌\1 ' ),
			( re.compile(r'\s+(گار)\s+', flags=re.DOTALL), r'‌\1 ' )
		]

		self._fix_prefix = fix_prefix
		self._fix_prefix_pattern = [
			re.compile(r'\s+(نا)\s+', flags=re.DOTALL),
			re.compile(r'\s+(غیر)\s+', flags=re.DOTALL),
			re.compile(r'\s+(بی)\s+', flags=re.DOTALL),
			re.compile(r'\s+(فرا)\s+', flags=re.DOTALL),
			re.compile(r'\s+(عدم)\s+', flags=re.DOTALL),
			re.compile(r'\s+(سوء)\s+', flags=re.DOTALL),
			re.compile(r'\s+(سوأ)\s+', flags=re.DOTALL)
		]

	def cleanup(self, text):
		# removing URLS bringing them back at the end of process
		urls = []
		pattern = r'https?:\/\/([-\w\.]+)+(:\d+)?(\/([\w\/_\.]*(\?\S+)?)?)?'
		iterator = re.finditer(pattern, text)
		for i, match in enumerate(iterator):
			urls.append(match.group(0))
			text = text.replace(match.group(0), "__urls__" + str(i) + "__", 1)
		
		if (self._fix_dashes):
			text = self.fix_dashes(text)
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

		# should not replace exnglish chars in english phrases
		pattern = r'([a-zA-Z\-_]{2,}[۰-۹]+|[۰-۹]+[a-zA-Z\-_]{2,})'
		iterator = re.finditer(pattern, text, flags=re.IGNORECASE)
		for match in iterator:
			new_text = match.group(0).translate(str.maketrans(self.persian_numbers, self.english_numbers))
			text.replace(match.group(0), new_text, 1)

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
		if (self._fix_suffix):
			text = self.fix_suffix(text)
		if (self._fix_prefix):
			text = self.fix_prefix(text)

		# bringing back urls
		pattern = r'__urls__\d+__'
		iterator = re.finditer(pattern, text)
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
		for pattern, rep in self._fix_dashes_pattern:
			text = pattern.sub(rep, text)
		return text

	def fix_three_dots(self, text):
		"""
			replace three dots with ellipsis

			>>> fix_three_dots('1, 2, 3, ..., 10')
			'1, 2, 3,…, 10'
		"""
		return self._fix_three_dots_pattern.sub('…', text)

	def fix_english_quotes(self, text):
		"""
			replace English quotes with their Persian equivalent
		"""
		return self._fix_english_quotes_ppattern.sub(r'«\2»', text)

	def fix_hamzeh(self, text):
		"""
			should convert ه ی to ه
		"""
		# \s	any whitespace (space, tab, line break)
		# \S	any character except whitespace
		return self._fix_hamzeh_pattern.sub(r'\1هٔ\3', text)

	def cleanup_zwnj(self, text):
		"""
			remove unnecessary zwnj char that are succeeded/preceded by a space
		"""
		return self._cleanup_zwnj_pattern.sub(' ', text)

	def fix_spacing_for_braces_and_quotes(self, text):
		for pattern, rep in self._fix_spacing_for_braces_and_quotes_pattern:
			text = pattern.sub(rep, text)
		return text

	def fix_english_numbers(self, text):
		"""
			>>> fix_english_numbers('1234-۱۲۳۴-١٢٣٤')
			'۱۲۳۴-۱۲۳۴-١٢٣٤'
		"""
		return text.translate(str.maketrans(self.english_numbers, self.persian_numbers))

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
		return self._fix_perfix_spacing_pattern.sub(r' \1‌', text)

	def fix_suffix_spacing(self, text):
		"""
			put zwnj between word and suffix (*tar *tarin *ha *haye)
			there's a possible bug here: های and تر could be separate nouns and not suffix
		"""
		return self._fix_suffix_spacing_pattern.sub(r'‌\1 ', text)

	def cleanup_extra_marks(self, text):
		"""
			replace more than one ! or ? mark with just one

			>>> cleanup_extra_marks('نه!!!!!')
			'نه!'
		"""
		for pattern in self._cleanup_extra_marks_pattern:
			text = pattern.sub(r'\1', text)
		return text

	def cleanup_kashidas(self, text):
		"""
			should remove all kashida (کشیده)

			>>> cleanup_kashidas('رحــــــيم')
			'رحيم'
		"""
		return self._cleanup_kashidas_pattern.sub('', text)

	def cleanup_spacing(self, text):
		"""
			should replace more than one space with just a single one
		"""
		for pattern, rep in self._cleanup_spacing_pattern:
			text = pattern.sub(rep, text)
		return text

	def cleanup_begin_and_end(self, text):
		"""
			remove spaces, tabs, and new lines from the beginning and enf of file
		"""
		return text.strip()

	def fix_suffix(self, text):
		for pattern, rep in self._fix_suffix_pattern:
			text = pattern.sub(rep, text)
		return text

	def fix_prefix(self, text):
		for pattern in self._fix_prefix_pattern:
			text = pattern.sub(r'‌ \1‌', text)
		return text

if __name__ == '__main__':
	normalizer = PersianTextNormalizer()
	text = ".واحد رسانه هاي خارجي همشهري: دولت ژاپن بودجه سال آينده كشور را تصويب كرد. بودجه 680 ميليارد دلاري ژاپن نشان دهنده 3 درصد افزايش  نسبت به امسال است. تحليلگران تدوين اين بودجه را تلاش محتاطانه دولت  براي تقويت بهبود اقتصادي خواندند.  به گزارش تلويزيون سي ان ان، از اوائل سال آينده ماليات بر مصرف در ژاپن از 3 درصدبه 5 درصد افزايش مي يابد برخي كارشناسان انجام  اين تغيير را داراي اثرات زياد بر اقتصاد ارزيابي مي كنند. برخي  كارشناسان رشد اقتصادي سال آينده ژاپن را بين 5/0 تا 5/2 درصد پيش بيني مي كنند و دولت رقم 9/1 درصد را برآورد مي كند.  ابهام در مورد رشد اقتصادي سال آينده كشورتا حدي بر بازار سهام  ژاپن اثر منفي گذاشت در پايان هفته 3 درصد از ارزش شاخص بورس توكيو نسبت به اول هفته كاهش يافت. من شمردم یک دو سه و ... تا به صد رسیدم. من غذا می خورم. تو غذا نمی‌خورم."
	normal_text = normalizer.cleanup(text)
	print (normal_text)
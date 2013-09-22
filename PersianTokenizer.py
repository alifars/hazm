import re

class PersianTokenizer():
	def __init__(self):
		# \u2e2e : arabic question mark 
		# \u061f: persian question mark
		# \u200c: ZERO WIDTH NON-JOINER (ZWNJ)
		self._sentence_pattern = re.compile(r'([\.\!\?\u2e2e\u061f][\"\'\u200c]?)\s+', flags=re.DOTALL)

		punc = r'!"\'\(\),،\.:؛;«»\?؟\[\]`\{\}'

		# \Z 		match at end of string
		self._word_patterns = [
			(
				re.compile('([^' + punc + '])([' + punc + '][' + punc + r'\s\u200c]|[' + punc + r']\Z)', flags=re.DOTALL),
				r'\1 \2'
			),
			(
				re.compile('([^' + punc + '])([' + punc + '][' + punc + r'\s\u200c]|[' + punc + r']\Z)', flags=re.DOTALL),
				r'\1 \2'
			),
			(
				re.compile(r'(\A[' + punc + r']|[' + punc + r'\s\u200C][' + punc + '])([^' + punc + '])', flags=re.DOTALL),
				r'\1 \2'
			),
			(
				re.compile('([' + punc + r'])(\?!\1)', flags=re.DOTALL),
				r'\1 \2'
			),
			(
				re.compile(r'[ \u200c]{2,}', flags=re.DOTALL),
				r' '
			)
		]

	def sent_tokenize(self, text):
		return self._sentence_pattern.sub(r'\1\n', text)

	def word_tokenize(self, text):
		for pattern, rep in self._word_patterns:
			text = pattern.sub(rep, text)
		return text

#def normalize(text):

if __name__ == '__main__':
	tokenizer = PersianTokenizer()
	text = ".واحد رسانه هاي خارجي همشهري: دولت ژاپن بودجه سال آينده كشور را تصويب كرد. بودجه 680 ميليارد دلاري ژاپن نشان دهنده 3 درصد افزايش  نسبت به امسال است. تحليلگران تدوين اين بودجه را تلاش محتاطانه دولت  براي تقويت بهبود اقتصادي خواندند.  به گزارش تلويزيون سي ان ان، از اوائل سال آينده ماليات بر مصرف در ژاپن از 3 درصدبه 5 درصد افزايش مي يابد برخي كارشناسان انجام  اين تغيير را داراي اثرات زياد بر اقتصاد ارزيابي مي كنند. برخي  كارشناسان رشد اقتصادي سال آينده ژاپن را بين 5/0 تا 5/2 درصد پيش بيني مي كنند و دولت رقم 9/1 درصد را برآورد مي كند.  ابهام در مورد رشد اقتصادي سال آينده كشورتا حدي بر بازار سهام  ژاپن اثر منفي گذاشت در پايان هفته 3 درصد از ارزش شاخص بورس توكيو نسبت به اول هفته كاهش يافت. من شمردم یک دو سه و ... تا به صد رسیدم. من غذا می خورم. تو غذا نمی‌خورم."
	sents = tokenizer.sent_tokenize(text)
	words = tokenizer.word_tokenize(sents)
	for sent in words.split('\n'):
		s.split(' ')
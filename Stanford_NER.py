from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
from nltk import Tree

class STANFORD:

	def __init__(self, text):
		self.text = text

	def extract(self):
		st = StanfordNERTagger('assets/english.all.3class.distsim.crf.ser.gz',
					   'assets/stanford-ner-4.0.0.jar',
					   encoding='utf-8')
		tokenized_text = word_tokenize(self.text)
		classified_text = st.tag(tokenized_text)

		entities = {}

		for item in classified_text:
			if item[1] != 'O':
				entities[item[0]] = item[1]

		return entities

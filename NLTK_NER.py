import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk import ne_chunk
from nltk import Tree
import re

class NLTK:

	def __init__(self, text):
		self.text = text

	def tokenize(self, text_string):   #split a string into tokens
		tokens = word_tokenize(text_string)
		return tokens

	def remove_stop_words(self, tagged):
    # define stop words
		stop_words = set(stopwords.words('english'))
    # filter text
		filtered_sentence = [w for w in tagged if w[0] not in stop_words]           # w = (word_token, pos)

		return filtered_sentence

	def stem(self, word_tokens):  #stem the words
		ps = PorterStemmer()
		for word_token in word_tokens:
			yield ps.stem(word_token)


	def lemma(self, word_tokens):  #lemma the words
	    lemmatizer = WordNetLemmatizer()
	    return [lemmatizer.lemmatize(word_token) for word_token in word_tokens]

	def pos_tagging(self, word_tokens):     #POS tagging
	    return pos_tag(word_tokens)

	def remove_hex_from_string(self, word_token):   #Remove hex number from string.
	    return re.sub(r'[0-9][A-F]', r'', word_token)

	def get_entities_from_pos_tagged(self, pos_tagged_text):
	    """
	    NER tagging
	    Using the module ne_chunk of nltk library, this function implements NER tagging and classifies as NE all tokens that
	     have been labelled as PERSON, ORGANIZATION, and GPE
	    :param pos_tagged_text: a list of tokens after as retrieved from pos_tag function of nltk
	    :return: a dictionary of the entities found and the NER type {"word":"type",}
	    """

	    entities = {}

	    chunks = ne_chunk(pos_tagged_text)
	    for chunk in chunks:
	        if type(chunk) is Tree:
	            t = ' '.join(c[0] for c in chunk.leaves())
	            entities[t] = chunk.label()

	    return entities

	def extract(self):

	    # tokenize
	    tokens = self.tokenize(self.text)
	    tokens_remove = [self.remove_hex_from_string(x) for x in tokens]
	    #tokens = lemma(tokens)
	    tagged = self.pos_tagging(tokens_remove)
	    candidates = self.get_entities_from_pos_tagged(tagged)

	    return candidates

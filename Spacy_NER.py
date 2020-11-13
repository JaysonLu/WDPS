import spacy

class SPACY:

	def __init__(self, text):
		self.text = text

	def extract(self):
		pretrained_model = 'en_core_web_sm'
		nlp = spacy.load(pretrained_model)
		doc = nlp(self.text)

	    # create a list to store entities and a list to store the labels of them
		entities = {}
	    # identify the entities with the pretrained model from spacy
		for ent in doc.ents:
			if ent.label_ not in ["CARDINAL", "DATE", "QUANTITY", "TIME", "ORDINAL", "MONEY", "PERCENT", "QUANTITY"]:
				entities[ent.text] = ent.label_

		return entities
		
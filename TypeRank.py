import trident
import json
import requests
import xmltodict

KBPATH='assets/wikidata-20200203-truthy-uri-tridentdb'


class TypeRank:
	"""docstring for TypeRank"""
	def __init__(self):
		#self.db = trident.Db(KBPATH)
		self.type_map = {
            "PERSON"        : "Q215627",
            "NORP"          : "Q2221906",   
            "FAC"           : "Q811979",    # architectural structure
            "ORG"           : "Q43229",
            "GPE"           : "Q2221906", # Countries, cities, states
            "LOC"           : "Q2221906",  # Non-GPE locations, mountain ranges, bodies of water
            "LANGUAGE"      : "Q28923954" # language & languoid class
        }
		self.pass_type = ["PRODUCT", "EVENT", "WORK_OF_ART", "LAW"]

	def rank(self, metion, candidate_entity):
		for entity in candidate_entity:
			query = "SELECT * { " + entity + " wdt:P31/wdt:P279* ?category }"
			print(query)
			results = self.db.sparql(query)
			print(results)


	def urlRank(self, metion, candidate_entity, type):
		if type in self.pass_type:
			return candidate_entity
		endpoint = "https://query.wikidata.org/bigdata/namespace/wdq/sparql?query="
		res = []
		typestring = "http://www.wikidata.org/entity/" + self.type_map[type]
		for entity in candidate_entity:
			query = "SELECT * { " + entity + " wdt:P31/wdt:P279* ?category }"
			resp = requests.get(endpoint+query)
			try:
				tree = xmltodict.parse(resp.text)
				results = tree["sparql"]["results"]["result"]
				for result in results:
					category = result["binding"]["uri"]
					if category == typestring:
						res.append(entity)
			except Exception as e:
				continue
		if len(res) == 0:
			return candidate_entity
		return res


if __name__ == "__main__":
	tr = TypeRank()
	metion = "Nevada"
	candidate_entity = ['<http://www.wikidata.org/entity/Q51509350>', '<http://www.wikidata.org/entity/Q2730309>', '<http://www.wikidata.org/entity/Q3338813>', '<http://www.wikidata.org/entity/Q7003343>', '<http://www.wikidata.org/entity/Q14560098>', '<http://www.wikidata.org/entity/Q18017553>', '<http://www.wikidata.org/entity/Q2907906>', '<http://www.wikidata.org/entity/Q21646785>', '<http://www.wikidata.org/entity/Q37504016>', '<http://www.wikidata.org/entity/Q1829995>']
	type = "GPE"
	res = tr.urlRank(metion, candidate_entity, type)
	print(res)


# wdt:P31/wdt:P279*

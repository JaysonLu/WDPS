from elasticsearch import Elasticsearch
import json

class ES:
	"""docstring for ES"""
	def __init__(self):
		self.es = Elasticsearch()

	def query(self, metions):
		res = {}
		for mention in metions:
			p = { "query" : {  "match" : {  "schema_name" : mention  } } }
			response = self.es.search(index="wikidata_en", body=json.dumps(p), request_timeout=20)
			if response["hits"]["total"]["value"] > 0:
				res[mention] = [(hits["_id"], hits["_source"]["rdfs_label"]) for hits in response["hits"]["hits"]]
		return res

		
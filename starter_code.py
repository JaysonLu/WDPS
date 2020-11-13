from warcio.archiveiterator import ArchiveIterator
from Html2TextConveter import Html2TextConveter
from utils import *
from NLTK_NER import NLTK
from Spacy_NER import SPACY
from Stanford_NER import STANFORD
from es_query import ES
from TypeRank import TypeRank
from Similarity import Similarity
import argparse

es = ES()
tr = TypeRank()

def find_labels(payload):
    if validate_html(payload):
        return
    key = payload.rec_headers.get_header(KEYNAME)

    ## extract text from html file
    converter = Html2TextConveter(payload)
    text = converter.text()
    # only process English html file
    if not validate_text(text):
        return
    
    ## extract metion from text
    ner = None
    if NLP == "nltk":
        ner = NLTK(text)
    elif NLP == "spacy":
        ner = SPACY(text)
    elif NLP == "stanford":
        ner = STANFORD(text)
    else:
        print('NLP_method: nltk spacy stanford')
        sys.exit(0)

    metions = ner.extract()

    # query elasticsearch to get candidate entity
    candidate_entity = es.query(metions)
    # rank candidate entity
    for metion, pack in candidate_entity.items():
        ## type filter
        if type_bool:
            rank = tr.urlRank(metion, [item[0] for item in pack], metions[metion])
            rank_pack = [item for item in pack if item[0] in rank]
        else:
            rank_pack = pack
        ## compute similarity
        similarity_rank = []
        for item in rank_pack:
            sim = Similarity(metion, item[1])
            similarity_rank.append({"entity":item[0], "sim":sim.cosine_similarity()})
        similarity_rank.sort(key=lambda similarity: (similarity["sim"]), reverse=True)
        if len(similarity_rank) > 0:
            yield key, metion, similarity_rank[0]["entity"]

if __name__ == '__main__':
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument('INPUT', help='path to warc file')
    parser.add_argument('--NLP', help='spacy, nltk, stanford', default="spacy")
    parser.add_argument('--type', help='boolean to decide whether to use wikidata service', default=False)
    args = parser.parse_args()

    INPUT = args.INPUT
    NLP = args.NLP
    type_bool = args.type
    
    with open(INPUT, 'rb') as stream:
        for payload in ArchiveIterator(stream):
            for key, label, wikidata_id in find_labels(payload):
                print(key + '\t' + label + '\t' + wikidata_id)

    
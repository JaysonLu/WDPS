from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
import scipy
import numpy as np
import math

class Similarity:

    if_brown_corpus = False
    if_load_wordnet = False
    embeddings = {}

    def __init__(self, text1, text2):
        self.text1 = text1
        self.text2 = text2

    def jaccard_similarirty(self):
        '''
        calculates Jaccard Similarity score
        '''
        try:

            t1 = set(self.text1.split(' '))
            t2 = set(self.text2.split(' '))

            intersection = set(t1 & t2)
            union = t1 | t2

            return len(intersection) / len(union)

        except Exception as e:
            return 0

    def cosine_similarity(self):
        '''
        calculate cosine similarity between two entities (stings)
        '''

        # convert words in "entity" to vectors
        t1 = self.word2vec(self.text1)
        t2 = self.word2vec(self.text2)

        try:
            sumxx = 0
            sumxy = 0
            sumyy = 0
            for i in range(len(t1)):
                x = t1[i]
                y = t2[i]
                sumxx += x * x
                sumyy += y * y
                sumxy += x * y

            return sumxy / math.sqrt(sumxx * sumyy)

        except Exception as e:
            return 0

    def word2vec(self, text):
        '''
        convert the extracted entity to a vector of numbers
        '''
        ent_vec = 0
        for i in text.split():

            # if word is not already in embeddings, generate a list of numbers between -1 and 1
            if i not in self.embeddings:
                word_vec = np.array(np.random.uniform(-1.0, 1.0, 100))
                self.embeddings[i] = word_vec
            # if the word is already in the embeddings, use the existing vector
            else:
                word_vec = self.embeddings[i]
            ent_vec = ent_vec + word_vec

        return ent_vec

    def wordnet_similarity(self):
        '''
        calculate Resnik similarity based on the Information Content
        wordnet is used
        can only be use to compare words (labels in the case of this assignment)
        '''

        # check if package is loaded
        if not self.if_load_wordnet:
            self.download_wordnet()
        if not self.if_brown_corpus:
            self.load_corpus()

        try:
            t1_lemma = self.lemmatize(self.text1)
            t2_lemma = self.lemmatize(self.text2)
            t1 = wn.synset(t1_lemma + '.n.01')
            t2 = wn.synset(t2_lemma + '.n.01')
            return t1.res_similarity(t2, self.brown_ic)

        except Exception as e:

            return 0

    def load_corpus(self):
        '''
        load corpus for wordnet
        '''

        self.brown_ic = wordnet_ic.ic('ic-brown.dat')
        self.if_brown_corpus = True

    def download_wordnet(self):
        nltk.download('wordnet')
        self.if_load_wordnet = True

    def lemmatize(self, word):
        lmtzr = WordNetLemmatizer()
        return lmtzr.lemmatize(word)


if __name__ == "__main__":
    t1 = 'Vrije Universiteit Amsterdam, tuin'
    t2 = 'Vrije Universiteit Brussels, hoofdgebouw'

    # t1 = 'watermelon'
    # t2 = 'im eating a watermelon'
    sim = Similarity(t1, t2)

    print(sim.cosine_similarity())

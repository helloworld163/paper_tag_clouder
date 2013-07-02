#!/usr/bin/env python

import nltk
import sys

#from nltk.corpus import stopwords

def leaves(tree):
  """Finds NP (nounphrase) leaf nodes of a chunk tree."""
  for subtree in tree.subtrees(filter = lambda t: t.node=='NP'):
    yield subtree.leaves()

def normalize(word, lemmatizer):
  """Normalises words to lowercase and stems and lemmatizes it."""
  word = word.lower()
  #word = stemmer.stem_word(word)
  word = lemmatizer.lemmatize(word)
  return word

def acceptable_word(word, stopwords):
  """Checks conditions for acceptable word: length, stopword."""
  accepted = bool(2 <= len(word) <= 40 and word.lower() not in stopwords)
  return accepted


def get_terms(tree, lemmatizer, stopwords):
  for leaf in leaves(tree):
    term = [ normalize(w, lemmatizer) for w,t in leaf if acceptable_word(w, stopwords) ]
    yield term

def get_nouns_and_noun_phrases(text):
  # Used when tokenizing words
  sentence_re = r'''(?x)    # set flag to allow verbose regexps
    ([A-Z])(\.[A-Z])+\.?  # abbreviations, e.g. U.S.A.
    | \w+(-\w+)*      # words with optional internal hyphens
    | \$?\d+(\.\d+)?%?    # currency and percentages, e.g. $12.40, 82%
    | \.\.\.        # ellipsis
    | [][.,;"'?():-_`]    # these are separate tokens
  '''

  lemmatizer = nltk.WordNetLemmatizer()
  #stemmer = nltk.stem.porter.PorterStemmer()

  #Taken from Su Nam Kim Paper...
  grammar = r"""
    NBAR:
      {<NN.*|JJ>*<NN.*>}  # Nouns and Adjectives, terminated with Nouns

    NP:
      {<NBAR>}
      {<NBAR><IN><NBAR>}  # Above, connected with in/of/etc...
  """
  chunker = nltk.RegexpParser(grammar)

  toks = nltk.regexp_tokenize(text, sentence_re)
  postoks = nltk.tag.pos_tag(toks)

  tree = chunker.parse(postoks)

  stopwords = nltk.corpus.stopwords.words('english')
  terms = get_terms(tree, lemmatizer, stopwords)
  return terms

def main(argv):
  pass

if __name__ == "__main__":
  main(sys.argv)

from nose.tools import assert_in

class TestAll():
  def test_get_nouns_and_noun_phrases(self):
    text = '''Models of document indexing and document retrieval have been extensively studied. The integration of these two classes of models has been the goal of several researchers but it is a very difficult problem. We argue that much of the reason for this is the lack of an adequate indexing model. This suggests that perhaps a better indexing model would help solve the problem. However, we feel that making unwarranted parametric assumptions will not lead to better retrieval performance. Furthermore, making prior assumptions about the similarity of documents is not warranted either. Instead, we propose an approach to retrieval based on probabilistic language modeling. We estimate models for each document individually. Our approach to modeling is non-parametric and integrates document indexing and document retrieval into a single model. One advantage of our approach is that collection statistics which are used heuristically in many other retrieval models are an integral part of our model.'''
    terms = get_nouns_and_noun_phrases(text)
    real_nouns = ['model', 'document', 'document retrieval', 'integration',
        'class', 'goal', 'several researcher', 'difficult problem', 'reason', 
        'lack', 'adequate indexing model', 'indexing model', 'problem', 
        'parametric assumption', 'retrieval performance', 'furthermore', 
        'assumption', 'similarity', 'instead', 'approach', 'retrieval',
        'probabilistic language', 'modeling', 'integrates document', 
        'single model', 'advantage', 'collection statistic',
        'many retrieval model', 'integral part']
    for t in terms:
      assert_in(' '.join(t), real_nouns)



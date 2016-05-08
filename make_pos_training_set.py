"""Convert multiple XML treebanks into pos list of list of tuples of two strings.

TODO: Correct any tuples that look like this: `('.', None)`. The None breaks the CRF tagger. This example arises
from the NLTK reader which produces this None when reading (at least) these words: `σωτῆρι/n-s---md- . .,/---------`.

TODO: Remove all question marks (?).

TODO: This is screwed up: `δαιμόνων/n-pἀντῴη---mg-`.

TODO: Consider removing all "?" forms and all punct (at least commas) too.

"""

from cltk.corpus.greek.beta_to_unicode import Replacer
from lxml import etree

__author__ = ['Kyle P. Johnson <kyle@kyle-p-johnson.com>', 'Stephen Margheim <stephen.margheim@gmail.com>']
__license__ = 'MIT License. See LICENSE.'


def get_tags():
    r = Replacer()
    entire_treebank = 'greek_treebank_perseus/agdt-1.7.xml'
    with open(entire_treebank, 'r') as f:
        xml_string = f.read()
    root = etree.fromstring(xml_string)
    sentences = root.findall('sentence')

    sentences_list = []
    for sentence in sentences:  # note: sentence is Element
        words_list = sentence.findall('word')
        sentence_list = []
        # http://ilk.uvt.nl/conll/
        for x in words_list:  # note: word is class
            word = x.attrib
            #id = word['id']
            form = word['form'].upper()  # make upper case for Beta Code converter
            form = r.beta_code(form)
            try:  # convert final sigmas
                if form[-1] == 'σ':
                    form = form[:-1] + 'ς'
            except IndexError:
                pass
            form = form.lower()

            # rm nasty single quotes
            form_list = [char for char in form if char not in [' ', "'", '᾽', '’', '[', ']']]
            form = ''.join(form_list)

            #lemma = word['lemma']
            #cpostag = word['relation']  # Coarse-grained part-of-speech tag
            postag = word['postag']
            #feats = '_'  # an underscore if not available
            #head = word['head']
            #deprel = word['head']
            #phead = '_'
            #pderprel = '_'
            if len(form) == 0: continue

            word_tag = '/'.join([form, postag])
            sentence_list.append(word_tag)
        sentence_str = ' '.join(sentence_list)
        sentences_list.append(sentence_str)
    treebank_training_set = '\n\n'.join(sentences_list)

    with open('greek_training_set.pos', 'w') as f:
        f.write(treebank_training_set)


def main():
    get_tags()


if __name__ == "__main__":
    main()

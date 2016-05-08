# -*- coding: utf-8 -*- 

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
            form_list = [char for char in form if char not in ["'", '᾽', '’', '[', ']']]
            form = ''.join(form_list)

            #lemma = word['lemma']
            cpostag = word['relation']  # Coarse-grained part-of-speech tag
            cpostag = cpostag.split('_')[0]

            #postag = word['postag']
            #feats = '_'  # an underscore if not available
            #head = word['head']
            #deprel = word['head']
            #phead = '_'
            #pderprel = '_'
            word_tag = '/'.join([form, cpostag])
            sentence_list.append(word_tag)
        sentence_str = ' '.join(sentence_list)
        sentences_list.append(sentence_str)
        
    treebank_training_set = '\n\n'.join(sentences_list)

    with open('penn_pos_training_set_reduce.pos', 'w') as f:
        f.write(treebank_training_set)


def main():
    get_tags()


if __name__ == "__main__":
    main()

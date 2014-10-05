from cltk.corpus.classical_greek.beta_to_unicode import Replacer
from lxml import etree
import os


__author__ = ['Kyle P. Johnson <kyle@kyle-p-johnson.com>', 'Stephen Margheim <stephen.margheim@gmail.com>']
__license__ = 'MIT License. See LICENSE.'


r = Replacer()


def get_files():
    """Return a Generator of the Perseus Greek Treebank XML files
    
    """
    files = os.listdir('treebank_perseus_greek')
    for file in files:
        if file.endswith('.xml'):
            yield file


def get_tags():
    treebank_training_set = []
    for xml_file in get_files():
        file_path = os.path.join('treebank_perseus_greek/', xml_file)
        with open(file_path, 'r') as f:
            xml_string = f.read()
        root = etree.fromstring(xml_string)
        sentences = root.findall('sentence')

        sentences_list = []
        for sentence in sentences:  # note: sentence is Element
            words_list = sentence.findall('word')
            sentence_list = []
            for x in words_list:  #note: word is class
                word = x.attrib
                form = word['form'].upper()  # make upper case for Beta Code converter
                uni_form = r.beta_code(form)
                try:  # convert final sigmas
                    if uni_form[-1] == 'σ':
                        uni_form = uni_form[:-1] + 'ς'
                except IndexError:
                    pass
                postag = word['postag']  # note: postag is str
                word_tag = '/'.join([uni_form, postag])
                sentence_list.append(word_tag)
            tagged_sentence = ' '.join(sentence_list)
            sentences_list.append(tagged_sentence)
        tagged_sentences = '\n\n'.join(sentences_list)
        treebank_training_set.append(tagged_sentences)
    pos_training_set = '\n\n'.join(treebank_training_set)

    with open('pos_training_set.pos', 'w') as f:
        f.write(pos_training_set)


def main():
    get_tags()


if __name__ == "__main__":
    main()

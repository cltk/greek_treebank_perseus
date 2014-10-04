from cltk.corpus.classical_greek.beta_to_unicode import Replacer
from lxml import etree
import os


r = Replacer()


def get_files():
    files = os.listdir('treebank_perseus_greek')
    xml_files_list = []
    for file in files:
        if file[-4:] == '.xml':
            xml_files_list.append(file)
    return xml_files_list


def get_tags(xml_files_list):
    treebank_training_set = []
    for xml_file in xml_files_list:
        with open('treebank_perseus_greek/' + xml_file) as f:
            xml_string = f.read()
        root = etree.fromstring(xml_string)
        sentences = root.findall("sentence")

        sentences_list = []
        for sentence in sentences:  # note: sentence is Element
            words_list = sentence.findall("word")
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
                word_tag = uni_form + '/' + postag
                sentence_list.append(word_tag)
            tagged_sentence = ' '.join(sentence_list)
            sentences_list.append(tagged_sentence)
        tagged_sentences = '\n\n'.join(sentences_list)
        treebank_training_set.append(tagged_sentences)
    pos_training_set = '\n\n'.join(treebank_training_set)

    with open('pos_training_set.txt', 'w') as f:
        f.write(pos_training_set)


def main():
    files = get_files()
    get_tags(files)


if __name__ == "__main__":
    main()

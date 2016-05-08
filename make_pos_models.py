"""Train cltk POS models from a training set and save them in the model repository."""

from nltk.corpus.reader import TaggedCorpusReader
from nltk.tag import UnigramTagger
from nltk.tag import BigramTagger
from nltk.tag import CRFTagger
from nltk.tag import TrigramTagger
from nltk.tag import tnt
import os
import pickle
import time


def make_pos_model(model_type):
    """Load selected algorithm, save model to models repo."""
    now = time.time()

    reader = TaggedCorpusReader('.', 'greek_training_set.pos')
    train_sents = reader.tagged_sents()
    if model_type == 'unigram':
        tagger = UnigramTagger(train_sents)
        file = 'unigram.pickle'
    elif model_type == 'bigram':
        tagger = BigramTagger(train_sents)
        file = 'bigram.pickle'
    elif model_type == 'trigram':
        tagger = TrigramTagger(train_sents)
        file = 'trigram.pickle'
    elif model_type == 'backoff':
        tagger1 = UnigramTagger(train_sents)
        tagger2 = BigramTagger(train_sents, backoff=tagger1)
        tagger = TrigramTagger(train_sents, backoff=tagger2)
        file = '123grambackoff.pickle'
    elif model_type == 'tnt':
        tagger = tnt.TnT()
        tagger.train(train_sents)
        file = 'tnt.pickle'
    elif model_type == 'crf':
        tagger = CRFTagger()
        file = 'crf.pickle'
        _dir = os.path.expanduser('~/greek_models_cltk/taggers/pos')
        path = os.path.join(_dir, file)
        tagger.train(train_sents, path)
        print('Completed training {0} model in {1} seconds to {2}.'.format(model_type, time.time() - now, path))
        return
    else:
        print('Invalid model_type.')

    _dir = os.path.expanduser('~/greek_models_cltk/taggers/pos')
    path = os.path.join(_dir, file)
    with open(path, 'wb') as f:
        pickle.dump(tagger, f)

    print('Completed training {0} model in {1} seconds to {2}.'.format(model_type, time.time() - now, path))

    #print('Accuracy:', tagger.evaluate(train_sents))

if __name__ == "__main__":
    # make_pos_model('unigram')
    # make_pos_model('bigram')
    # make_pos_model('trigram')
    # make_pos_model('backoff')
    # make_pos_model('tnt')
    make_pos_model('crf')

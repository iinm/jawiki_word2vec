# -*- coding: utf-8 -*-

import sys
import os
import cherrypy
import getopt
import json
import cPickle as pickle
import numpy
import gensim
from gensim import matutils

import tools


def mean_word_vecs(model, positive=[], negative=[], skip_unknown=False):
    '''
    gensim.Word2vecのモデルから、単語を足しあわせたベクトルを計算する。
    this code is based on gensim.Word2vec.most_simialr
    どの単語も辞書にない場合はNoneを返す。
    '''
    model.init_sims()

    # add weights for each word, if not already present; default to 1.0 for
    # positive and -1.0 for negative words
    positive = [(word, 1.0) for word in positive]
    negative = [(word, -1.0) for word in negative]

    # compute the weighted average of all words
    all_words, mean = set(), []
    for word, weight in positive + negative:
        if isinstance(word, numpy.ndarray):
            mean.append(weight * word)
        elif word in model.vocab:
            mean.append(weight * model.syn0norm[model.vocab[word].index])
            #all_words.add(model.vocab[word].index)
        elif not skip_unknown:
            words = tools.word_segmenter_ja(word, np=False)
            words = [w for w in words if len(w.strip()) > 0]
            mean_ = mean_word_vecs(model, positive=words, skip_unknown=True)
            if mean_ is not None:
                mean.append(weight * mean_)
            #raise KeyError("word '%s' not in vocabulary" % word)

    if not mean:
        #raise ValueError("cannot compute similarity with no input")
        return None

    mean = matutils.unitvec(numpy.array(mean).mean(axis=0)).astype(numpy.float32)
    return mean


class Word2VecServer(object):
    def __init__(self, model_fname):
        # load word vectors
        self.model = gensim.models.Word2Vec.load(model_fname)

    def index(self, positive=u'', negative=u'', skip_unknown=u''):
        positive = positive.split(u',') if len(positive) > 0 else []
        negative = negative.split(u',') if len(negative) > 0 else []
        skip_unknown = (skip_unknown == u'true')
        word_vec = mean_word_vecs(self.model, positive, negative, skip_unknown)
        return pickle.dumps(word_vec, pickle.HIGHEST_PROTOCOL)
    index.exposed = True


if __name__ == '__main__':
    options, args = getopt.getopt(sys.argv[1:], 'h:p:m:')
    options = dict(options)
    host, port = options['-h'], int(options['-p'])
    model_fname = options['-m']

    cherrypy.config.update({
        'server.socket_host': host,
        'server.socket_port': port
    })

    conf = {
        '/': {
            #'tools.response_headers.on': True,
            #'tools.response_headers.headers': [('Content-type', 'application/json')]
        }
    }
    cherrypy.quickstart(Word2VecServer(model_fname), '/', conf)

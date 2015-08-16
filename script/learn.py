#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import bz2
import gzip
import gensim
import logging

import data, tools


class Sentences(object):
    def __init__(self, data_root, test_=False):
        self.data_root = data_root
        self.test_ = test_

    def __iter__(self):
        for file_count, fname in enumerate(data.iter_files(self.data_root)):
            if self.test_ and file_count >= 100:
                break
            f = bz2.BZ2File(fname)
            for doc_str in data.iter_docs(f):
                doc_str = doc_str.decode('utf-8')
                sents = tools.sent_splitter_ja(doc_str, fix_parenthesis=True)
                for sent in sents:
                    sent = sent.strip()
                    if len(sent) == 0:
                        continue
                    words = tools.word_segmenter_ja(sent, baseform=False)
                    yield words
            f.close()


def test_iter_sentences(data_root):
    sentences = Sentences(data_root)
    for words in sentences:
        print '^', u'|'.join(words).encode('utf-8')


if __name__ == '__main__':

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                        level=logging.INFO)

    this_dirname = os.path.dirname(os.path.abspath(__file__))
    data_root = this_dirname + '/../data/extracted'
    #test_iter_sentences(data_root)

    sentences = Sentences(data_root)#, test_=True)
    model = gensim.models.Word2Vec(
        sentences, size=300, window=5, min_count=5, workers=8
    )

    model_fname = sys.argv[1]
    opener = gzip.open if model_fname.endswith('.gz') else open
    model_f = opener(sys.argv[1], 'w')
    model.save(model_f)

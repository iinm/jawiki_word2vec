#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import bz2

import tools


def iter_files(root):
    for dir_, subdirs, files in os.walk(root):
        files.sort()
        for fname in files:
            fname = os.path.join(dir_, fname)
            if not fname.endswith('.bz2'):
                continue
            yield fname


def iter_docs(f): # <- bz2.BZ2File('wiki_??.bz2')
    doc = ''
    for line in f:
        if line.startswith('<doc id'):
            doc = ''
        elif line.startswith('</doc>'):
            yield doc
        elif line.startswith('scroll=1'):
            # たまに本文以外が混ざってる
            continue
        else:
            doc += line


def test_iter_docs():
    data_root = os.path.dirname(os.path.abspath(__file__)) + '/../data/extracted'
    for fname in iter_files(data_root):
        f = bz2.BZ2File(fname)
        for doc_str in iter_docs(f):
            print '-' * 70
            #print doc_str
            doc_str = doc_str.decode('utf-8')
            sents = tools.sent_splitter_ja(doc_str)
            for sent in sents:
                words = tools.word_segmenter_ja(sent)
                print '^', u'|'.join(words).encode('utf-8')


if __name__ == '__main__':
    test_iter_docs()

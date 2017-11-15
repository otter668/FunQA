#!/usr/bin/python
# -*- coding: UTF-8 -*-

class Segmenter(object):
    def __init__(self, postagging, stopwords_set):
        self.ptag = postagging
        self.sws = stopwords_set

    def release(self):
        pass

    def load_userdict(self):
        pass

    def sent2words(self, sent):
        pass

    def _remove_stopwords(self, words):
        if self.sws:
            for word in words:
                if word.term in self.sws:
                    words.remove(word)
        return words
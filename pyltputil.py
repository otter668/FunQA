#!/usr/bin/python
# -*- coding: UTF-8 -*-
from segmenterutil import Segmenter
from sentences import Word
from pyltp import Segmentor, Postagger


class PyltpSegmenter(Segmenter):
    def __init__(self, postagging, stopwords_set):
        super(PyltpSegmenter, self).__init__(postagging, stopwords_set)
        self.segmenter = Segmentor()
        self.segmenter.load('ltp_data_v3.4.0/cws.model')
        if self.ptag:
            self.postagger = Postagger()
            self.postagger.load('ltp_data_v3.4.0/pos.model')

    def release(self):
        self.segmenter.release()
        if self.ptag:
            self.postagger.release()

    def load_userdict(self):
        self.segmenter.load_with_lexicon('ltp_data_v3.4.0/cws.model', 'data/dict.small.txt')

    def sent2words(self, sent):
        seg_words = self.segmenter.segment(sent)
        if self.ptag:
            postags = self.postagger.postag(seg_words)
            words = [Word(word, pos) for word, pos in zip(seg_words, postags)]
        else:
            words = [Word(word) for word in seg_words]
        # after word segment, the stop words will not print to the file
        return self._remove_stopwords(words)
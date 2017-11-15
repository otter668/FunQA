#!/usr/bin/python
# -*- coding: UTF-8 -*-
from segmenterutil import Segmenter
from sentences import Word
import jieba
import jieba.posseg as pseg


class JiebaSegmenter(Segmenter):
    def load_userdict(self):
        jieba.load_userdict('data/dict.small.txt')

    def sent2words(self, sent):
        if self.ptag:
            cut_words = pseg.cut(sent)
            words = [Word(word, pos) for word, pos in cut_words if word != ' ']
        else:
            cut_words = jieba.cut(sent)
            words = [Word(word) for word in cut_words if word != ' ']
        # after word segment, the stop words will not print to the file
        return self._remove_stopwords(words)
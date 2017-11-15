#!/usr/bin/python
# -*- coding: UTF-8 -*-
from segmenterutil import Segmenter
from sentences import Word
import pynlpir


class PyNLPIRSegmenter(Segmenter):
    def __init__(self, postagging, stopwords_set):
        super(PyNLPIRSegmenter, self).__init__(postagging, stopwords_set)
        pynlpir.open()

    def release(self):
        pynlpir.close()

    def load_userdict(self):
        pynlpir.nlpir.ImportUserDict(b'data/UserDic.dic', False)

    def sent2words(self, sent):
        seg_words = pynlpir.segment(sent, pos_tagging=self.ptag)
        if self.ptag:
            words = [Word(word, pos) for word, pos in seg_words if word != ' ']
        else:
            words = [Word(word) for word in seg_words if word != ' ']
        # after word segment, the stop words will not print to the file
        return self._remove_stopwords(words)

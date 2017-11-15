#!/usr/bin/python
# -*- coding: UTF-8 -*-
import argparse
import json
import sys
from sentences import Sentence


class Tokenizer(object):
    def __init__(self, tokenizer='pyltp', labeled=True, postagging=True):
        """

        :param tokenizer: which segmenter you choice
        :param labeled: the flag of line's label
        :param postagging: the flag of pos
        """
        # stop_words_fn is the file name of the stopwords file
        stop_words_fn = 'data/all_stopword'
        self.stopWords_set = self._get_stopwords(stop_words_fn)
        self.labeled = labeled
        self.postagging = postagging
        self.tokenizer_config = self._get_tokenizer_dict()
        self.tokenizer = self._get_tokenizer(tokenizer)
        # self.tokenizer.load_userdict()

    def __del__(self):
        try:
            self.stopWords_set.clear()
            self.tokenizer.release()
        except:
            pass

    # return a generator of lable and words in a sentce
    def __iter__(self):
        with sys.stdin as f:
            for line in f:
                if line.lstrip():
                    s = Sentence(line.strip(), self.labeled)
                    s.appendwords(self.tokenizer.sent2words(s.question))
                    yield s

    @staticmethod
    def _get_stopwords(stop_words_fn):
        try:
            with open(stop_words_fn, 'r', encoding='utf-8') as f:
                stop_words_set = {line.strip() for line in f}
            return stop_words_set
        except:
            return None

    @staticmethod
    def _get_tokenizer_dict():
        try:
            with open('tokenizer.cfg', 'r', encoding='utf-8') as f:
                tokenizer_dict = json.load(f)
            return tokenizer_dict
        except:
            return None

    def _get_tokenizer(self, tokenizer):
        try:
            cfg = self.tokenizer_config[tokenizer]
            seg_module = __import__(cfg['utilname'])
            return getattr(seg_module, cfg['classname'])(self.postagging, self.stopWords_set)
        except KeyError:
            print('The segmenter of {} that you chose does not exist!'.format(tokenizer), file=sys.stderr)
            sys.exit(1)


def main(tokenizer, labeled, postagging):
    token = Tokenizer(tokenizer, labeled, postagging)
    for sent in token:
        print(sent)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-s', '--segmenter', choices=['pyltp', 'jieba', 'pynlpir'], default='pyltp', help='choise a segmenter in (jieba, pynlpir, pyltp)')
    ap.add_argument('-l', '--labeled', action='store_true', help='whether contains labels in front of corpus')
    ap.add_argument('-p', '--postagging', action='store_true', help='whether to tagging pos label')
    # ap.add_argument('redirect', help="")
    # ap.add_argument('filename', help="The filename to be processed")
    args = ap.parse_args()
    # sys.stdin = open(args.filename, 'r', encoding='utf-8')
    main(args.segmenter, args.labeled, args.postagging)

#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import sys
from pyltp import Parser

def main(parser):
    with sys.stdin as f:
        for line in f:
            d = json.loads(line)
            words, postags = [], []
            for wordpos in d['words']:
                words.append(wordpos['term'])
                postags.append(wordpos['pos'])
            arcs = parser.parse(words, postags)
            for wordpos, arc in zip(d['words'], arcs):
                wordpos['head'] = arc.head
                wordpos['rel'] = arc.relation
            print(json.dumps(d))


if __name__ == '__main__':
    # sys.stdin = open(sys.argv[-1], 'r', encoding='utf-8')
    parser = Parser()
    parser.load('ltp_data_v3.4.0/parser.model')
    main(parser)
    parser.release()
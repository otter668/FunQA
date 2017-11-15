#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import sys
from pyltp import NamedEntityRecognizer

def main(recognizer):
    with sys.stdin as f:
        for line in f:
            d = json.loads(line)
            words, postags = [], []
            for wordpos in d['words']:
                words.append(wordpos['term'])
                postags.append(wordpos['pos'])
            netags = recognizer.recognize(words, postags)
            for wordpos, ne in zip(d['words'], netags):
                wordpos['ne'] = ne
            print(json.dumps(d))


if __name__ == '__main__':
    # sys.stdin = open(sys.argv[-1], 'r', encoding='utf-8')
    recognizer = NamedEntityRecognizer()
    recognizer.load('ltp_data_v3.4.0/ner.model')
    main(recognizer)
    recognizer.release()
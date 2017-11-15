#!/usr/bin/python
# -*- coding: UTF-8 -*-
import argparse
import json

import sys
from collections import Counter


def build_vocab(taxonomy, features):
    vocab = dict()
    vocab['label'] = []
    for feature in template[features]:
        vocab[feature] = []
    for line in sys.stdin:
        sent = json.loads(line)
        label = sent['label']
        if taxonomy:
            label = sent['label'][:sent['label'].index('_')]
        vocab['label'].append(label)
        for feature in [feature for feature in sent if feature != 'label']:
            vocab[feature].extend(sent[feature])
    vocab['label'] = Counter(vocab['label'])
    for feature in template[features]:
        vocab[feature] = Counter(vocab[feature])
    return vocab



def encoding(vocab, taxonomy):
    sys.stdin.seek(0, 0)
    features = [v for v in sorted(vocab) if v != 'label']
    offsets = [0]
    for f in features:
        offsets.append(offsets[-1] + len(vocab[f]))
    for line in sys.stdin:
        sent = json.loads(line)
        label = sent['label']
        if taxonomy:
            label = sent['label'][:sent['label'].index('_')]
        print(vocab['label'][label]['index'] + 1, end=' ')
        for feature, fname, offset in zip([sent[f] for f in features], features, offsets):
            f = ['{}:1'.format(index)
                 for index in sorted([vocab[fname][item]['index'] + offset + 1
                                      for item in set(feature)])]
            print(' '.join(f), end=' ')
        print()


def load_cfg(cfg):
    try:
        with open(cfg, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        print('Load Configation File Error!', file=sys.stderr)
        sys.exit(1)


def sort_vocab(vocab):
    for v in vocab:
        for i, key in enumerate(sorted(vocab[v])):
            vocab[v][key] = {
                'index': i,
                'freq': vocab[v][key]
            }
    return vocab


def main(taxonomy, features, outvocab):
    vocab = build_vocab(taxonomy, features)
    vocab = sort_vocab(vocab)
    if outvocab:
        for lab in vocab:
            with open('data/{}.vocab'.format(lab), 'w', encoding='utf-8') as f:
                for key in vocab[lab]:
                    print('{}, {}, {}'.format(key, vocab[lab][key]['index'], vocab[lab][key]['freq']), file=f)
    encoding(vocab, taxonomy)


template = load_cfg('features.cfg')
if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-t', '--taxonomy', action='store_true', help='classfication on fine or coarse, default:fine')
    ap.add_argument('-f', '--features', default='baseline', help='select features in ConfigurationFile')
    ap.add_argument('-o', '--output', action='store_true', help='whether output vocabulary in files, default:false')
    # ap.add_argument('redirect', help="")
    # ap.add_argument('filename', help="The filename to be processed")
    args = ap.parse_args()
    # sys.stdin = open(args.filename, 'r', encoding='utf-8')
    main(args.taxonomy, args.features, args.output)

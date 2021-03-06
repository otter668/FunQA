#!/usr/bin/python
# -*- coding: UTF-8 -*-
import argparse
import json

import sys
from collections import Counter


def build_vocab(taxonomy, features, filename):
    vocab = dict()
    vocab['label'] = []
    for feature in template[features]:
        vocab[feature] = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            sent = json.loads(line)
            label = sent['label']
            if taxonomy:
                label = sent['label'][:sent['label'].index('_')]
            vocab['label'].append(label)
            # for feature in [feature for feature in sent if feature != 'label']:
            for feature in sent:
                if feature != 'label':
                    vocab[feature].extend(sent[feature])
        vocab['label'] = Counter(vocab['label'])
        for feature in template[features]:
            vocab[feature] = Counter(vocab[feature])
    return vocab


def encoding(vocab, taxonomy, filename):
    features = [v for v in sorted(vocab) if v != 'label']
    offsets = [0]
    for ft in features:
        offsets.append(offsets[-1] + len(vocab[ft]))
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            sent = json.loads(line)
            label = sent['label']
            if taxonomy:
                label = sent['label'][:sent['label'].index('_')]
            print(vocab['label'][label]['index'] + 1, end=' ')
            for feature, fname, offset in zip([sent[ft] for ft in features], features, offsets):
                ftc = ['{}:1'.format(index)
                     for index in sorted([vocab[fname][item]['index'] + offset + 1
                                          for item in set(feature)])]
                print(' '.join(ftc), end=' ')
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


def main(taxonomy, features, outvocab, inputfile):
    vocab = build_vocab(taxonomy, features, inputfile)
    vocab = sort_vocab(vocab)
    if outvocab:
        perfix = inputfile.split('/')[-1]
        for lab in vocab:
            with open('data/{}_vocab'.format('_'.join((perfix, lab, 'coarse' if taxonomy else 'fine'))), 'w', encoding='utf-8') as f:
                for key in vocab[lab]:
                    print('{}, {}, {}'.format(key, vocab[lab][key]['index'], vocab[lab][key]['freq']), file=f)
    encoding(vocab, taxonomy, inputfile)


template = load_cfg('features.cfg')
if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-t', '--taxonomy', action='store_true', help='classfication on fine or coarse, default:fine')
    ap.add_argument('-f', '--features', default='baseline', help='select features in ConfigurationFile')
    ap.add_argument('-o', '--output', action='store_true', help='whether output vocabulary in files, default:false')
    ap.add_argument('-if', '--inputfile', help='The filename which to be processed')
    args = ap.parse_args()
    main(args.taxonomy, args.features, args.output, args.inputfile)

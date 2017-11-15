#!/usr/bin/python
# -*- coding: UTF-8 -*-
import argparse
import json

import sys
import cplxfeature


def load_cfg(cfg):
    try:
        with open(cfg, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        print('Load Configation File Error!', file=sys.stderr)
        sys.exit(1)


def main(features):
    template = load_cfg('features.cfg')
    with sys.stdin as f:
        for line in f:
            sent = json.loads(line)
            dict_sent = {}
            if 'label' in sent:
                dict_sent['label'] = sent['label']
            for k, feature in template[features].items():
                if not feature.startswith('@'):
                    dict_sent[k] = [word[feature] for word in sent['words']]
                else:
                    dict_sent[k] = getattr(cplxfeature, feature[1:])(sent['words'])
            print(json.dumps(dict_sent))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-f', '--features', default='baseline', help='select features in ConfigurationFile')
    # ap.add_argument('redirect', help="")
    # ap.add_argument('filename', help="The filename to be processed")
    args = ap.parse_args()
    # sys.stdin = open(args.filename, 'r', encoding='utf-8')
    main(args.features)

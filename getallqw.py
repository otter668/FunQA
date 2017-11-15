#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json


def main():
    qws = set()
    with open('data/seg++', 'r', encoding='utf-8') as f:
        for line in f:
            d = json.loads(line)
            wordlist = [words['term'] for words in d['words'] if words['pos'] == 'r']
            qws.update(wordlist)
    for qw in qws:
        print(qw)


def distinct():
    qws = set()
    with open('data/interrogative', 'r', encoding='utf-8') as f:
        for line in f:
            qws.add(line.strip())
    for qw in sorted(qws):
        print(qw)


if __name__ == '__main__':
    # main()
    distinct()
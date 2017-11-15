#!/usr/bin/python
# -*- coding: UTF-8 -*-
import argparse
import linecache
from random import shuffle


def seq_split(file, splitpoint):
    outputfiles = ['{}_{}'.format(file, i+1) for i in range(len(splitpoint))]
    data = linecache.getlines(file)
    index = 0
    for name, sp in zip(outputfiles, splitpoint):
        with open(name, 'w', encoding='utf-8') as f:
            for i in range(sp):
                print(data[index].strip(), file=f)
                index += 1


def random_split(file, splitpoint):
    outputfiles = ['{}_{}'.format(file, i+1) for i in range(len(splitpoint))]
    data = linecache.getlines(file)
    shuffle(data)
    index = 0
    for name, sp in zip(outputfiles, splitpoint):
        with open(name, 'w', encoding='utf-8') as f:
            for i in range(sp):
                print(data[index].strip(), file=f)
                index += 1


def tag_split(file, splitpoint):
    data_dict = dict()
    data = linecache.getlines(file)
    for line in data:
        key, value = line.strip()[:line.index(' ')], line.strip()[line.index(' ')+1:]
        if key not in data_dict:
            data_dict[key] = []
        data_dict[key].append(value)
    del data
    linecache.clearcache()
    for name in sorted(data_dict.keys()):
        with open('{}_{}'.format(file, name), 'w', encoding='utf-8') as f:
            for value in data_dict[name]:
                print(' '.join([name, value]), file=f)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-f', '--file', help='the file to be split')
    ap.add_argument('-sp', '--splitpoint', help='the file of splitpoint')
    ap.add_argument('-s', '--sequence', choices=['seq', 'ran', 'tag'], default='seq',
                    help='the order[seq, ran, tag] in outputfile, default:seq')
    args = ap.parse_args()
    sp = []
    with open(args.splitpoint, 'r', encoding='utf-8') as f:
        for line in f:
            if line.lstrip():
                sp.append(int(line.strip()))
    distributor={'seq': seq_split, 'ran': random_split, 'tag': tag_split}
    distributor[args.sequence](args.file, sp)

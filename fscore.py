#!/usr/bin/python
# -*- coding: UTF-8 -*-
import argparse
import os
from collections import Counter


class Data(object):
    labs = []
    questions = []
    perdicts = dict()

    def __init__(self, test_file, taxonomy):
        with open(test_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if taxonomy == 'coarse':
                    self.labs.append(line[:line.find('_')])
                else:
                    self.labs.append(line[:line.find(' ')])
                self.questions.append(line[line.find(' ') + 1:])
        self.labs_tp_fn = Counter(self.labs)

    def append(self, pfs):
        predict = []
        vocab = dict()
        trainingset = dict()
        with open(pfs['result'], 'r', encoding='utf-8') as rf, open(pfs['labs'], 'r', encoding='utf-8') as lf:
            for line in rf:
                predict.append(line.strip())
            for line in lf:
                parts = line.strip().split(',')
                vocab[int(parts[1])] = parts[0]
                trainingset[parts[0]] = parts[2].strip()
        name = pfs['result'].split('/')[-1].split('_')[0]
        self.perdicts[name] = {'perdict': predict, 'vocab': vocab, 'ts': trainingset}


class Result(object):

    def __init__(self):
        self.label = ''
        self.question = ''
        self.perdict = ''

    def __str__(self):
        return '{}\t{}\t{}'.format(self.label, self.perdict, self.question)

    def equals(self):
        return self.label == self.perdict
    pass


class Analyzer(object):
    path = 'data/'
    all_items = dict()
    all_labs_tp = dict()
    all_labs_tp_fp = dict()
    result_dict = dict()

    def __init__(self, test_file_name, prefix_result_file, taxonomy):
        self.test_file = ''.join((self.path, test_file_name))
        self.data = Data(self.test_file, taxonomy)
        results = []
        labs = []
        for file_name in os.listdir(self.path):
            parts_file_name = file_name.split('_')
            if file_name.startswith(prefix_result_file) and file_name.endswith('result'):
                if taxonomy in parts_file_name:
                    results.append(''.join((self.path, file_name)))
            if file_name.startswith(prefix_result_file) and file_name.endswith('vocab'):
                if 'label' in parts_file_name:
                    if taxonomy in parts_file_name:
                        labs.append(''.join((self.path, file_name)))
        for item in zip(sorted(results), sorted(labs)):
            self.data.append({'result': item[0], 'labs': item[1]})
        pass

    def count(self):
        self.all_labs_tp_fn = self.data.labs_tp_fn
        for key in self.data.perdicts:
            items = []
            items_tp = []
            for label, question, perdict in zip(self.data.labs, self.data.questions, self.data.perdicts[key]['perdict']):
                item = Result()
                item.label = label
                item.question = question
                item.perdict = self.data.perdicts[key]['vocab'][int(perdict) - 1]
                items.append(item)
                if item.equals():
                    items_tp.append(label)
            self.all_items[key] = items
            self.all_labs_tp[key] = Counter(items_tp)
            self.all_labs_tp_fp[key] = Counter([item.perdict for item in items])
        pass


    def print_info(self):
        for key in self.data.perdicts:
            print(key, end='\t')
            tps = sum(self.all_labs_tp[key].values())
            count = len(self.all_items[key])
            print('Accuracy={:.4%} ({}/{})'.format(tps/count, tps, count))
            for label in self.all_labs_tp_fn:
                print(' '.join((label, self.data.perdicts[key]['ts'][label])), end='')
                tp = self.all_labs_tp[key][label]
                tp_fp = self.all_labs_tp_fp[key][label]
                tp_fn = self.all_labs_tp_fn[label]
                if tp_fp!=0:
                    print(' Precision={0:.4%} ({1}/{2}) Recall={3:.4%} ({1}/{4}) F1-Measure={5:.4%}'.format(
                        tp/tp_fp, tp, tp_fp, tp/tp_fn, tp_fn, 2*tp/(tp_fp+tp_fn)))
                else:
                    print(' Precision=0.0000% ({0}/{1}) Recall=0.0000% ({0}/{2}) F1-Measure=0%'.format(tp, tp_fp, tp_fn))

    def analyze(self):
        command = dict()
        command['lists'] = 'item.label == label'
        command['errors'] = 'not item.equals() and item.label == label'
        command['perdicts'] = 'item.perdict == label'
        print('<Training set>;<lists|errors|perdicts> {label}')
        print('Training set:\t', '\t'.join(key for key in self.data.perdicts))
        while(True):
            commandline = input('$ ')
            key = commandline.split(';')[0]
            action = commandline.split(';')[-1].split(' ')[0]
            label = commandline.split(';')[-1].split(' ')[-1]
            if key.lower().startswith('exit'):
                return
            for item in self.all_items[key]:
                if eval(command[action]):
                    print(item)


def main(test, results, taxonomy):
    alzr = Analyzer(test, results, taxonomy)
    alzr.count()
    alzr.print_info()
    alzr.analyze()
    pass


if __name__ == '__main__':
    ap = argparse.ArgumentParser(
        description='It is used to calculate accuracy, recall rate and F1 value, and result analysis.')
    ap.add_argument('test_file', help='the name of test file which contains labels and sentences.')
    ap.add_argument('result_file', help='the prefix of result files which generated by svm.')
    ap.add_argument('-t', '--taxonomy', default='fine', choices=('fine', 'coarse'),
                    help='the taxonomy of fine or coarse, default:fine')
    args = ap.parse_args()
    main(args.test_file, args.result_file, args.taxonomy)

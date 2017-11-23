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
    surfixs = ('', '+', '-', '+-')
    all_items = dict()
    all_labs_tp = dict()
    all_labs_tp_fp = dict()
    result_dict = dict()

    def __init__(self, test_file_name, prefix_result_file, taxonomy):
        self.test_file = ''.join((self.path, test_file_name))
        self.data = Data(self.test_file, taxonomy)
        results = []
        labs = []
        file_name_starts = [''.join((prefix_result_file, surfix)) for surfix in self.surfixs]
        for file_name in os.listdir(self.path):
            parts_file_name = file_name.split('_')
            if parts_file_name[0] in file_name_starts and file_name.endswith('result'):
                if taxonomy in parts_file_name:
                    results.append(''.join((self.path, file_name)))
            if parts_file_name[0] in file_name_starts and file_name.endswith('vocab'):
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
            sigma_tp_fp = 0
            print(key, end=' ')
            tps = sum(self.all_labs_tp[key].values())
            count = len(self.all_items[key])
            print('Accuracy={:.4%} ({}/{})'.format(tps/count, tps, count))
            print('\t'.join(('label', '#Train', '#Precision\t', '#Recall\t', '#F1-Measure')))
            for label in self.all_labs_tp_fn:
                print(' '.join((label, self.data.perdicts[key]['ts'][label])), end='\t')
                tp = self.all_labs_tp[key][label]
                tp_fp = self.all_labs_tp_fp[key][label]
                tp_fn = self.all_labs_tp_fn[label]
                p = 0
                if tp_fp!=0:
                    p = tp / tp_fp
                    sigma_tp_fp += tp_fp
                r = tp / tp_fn
                f = 2 * tp / (tp_fp + tp_fn)
                print('{0:.4%} ({1}/{2})\t{3:.4%} ({1}/{4})\t{5:.4%}'.format(p, tp, tp_fp, r, tp_fn, f))
            avg_p = tps/sigma_tp_fp
            avg_r = tps/count
            avg_f = 2 * avg_p * avg_r / (avg_p + avg_r)
            print('\t\t{:.4%}\t\t{:.4%}\t\t{:.4%}'.format(avg_p, avg_r, avg_f))

    def analyze(self):
        command = dict(list = lambda x,y:x.label == y,
                       error = lambda x,y: not x.equals() and x.label == y,
                       perdict = lambda x,y:x.perdict == y)
        # command['lists'] = 'item.label == label'
        # command['lists'] = lambda x,y:x==y
        # command['errors'] = 'not item.equals() and item.label == label'
        # command['perdicts'] = 'item.perdict == label'
        print('Usage: <label1[ label2[ labeln]];>|<exit>[action;][TrainingSet;]')
        print('labels see above. or exit')
        print('action: list, error, perdict')
        print('TrainingSet: ', ' '.join(key for key in self.data.perdicts))
        action = 'error'
        key = list(self.data.perdicts.keys())[-1]
        while(True):
            commandline = input('$ ')
            cmds = commandline.split(';')
            labels = cmds[0].strip().split(' ')
            if len(cmds) >= 2:
                action = cmds[1]
            if len(cmds) == 3:
                key = cmds[2]
            if labels[0].lower().startswith('exit'):
                return
            print('TrainingSet: ', ' '.join(key for key in self.data.perdicts))
            print('\t\t'.join(('TestSet', 'Perdict', 'Question')))
            for item in self.all_items[key]:
                for label in labels:
                    if command[action](item, label):
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

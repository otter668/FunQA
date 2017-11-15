#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json


class Sentence(object):
    def __init__(self, line, label):
        if label:
            self.label = line[:line.find(' ')]
            self.question = line[line.find(' ') + 1:]
        else:
            self.label = None
            self.question = line
        self.words = None

    def appendwords(self, words):
        self.words = words

    def __str__(self):
        sent = {}
        if self.label:
            sent['label'] = self.label
        # sent['question'] = self.question
        sent['words'] = [word.__dict__ for word in self.words]
        return json.dumps(sent)


class Word(object):
    def __init__(self, term, pos=None, ne=None, head=None, rel=None):
        self.term = term
        if pos:
            self.pos = pos
        if ne:
            self.ne = ne
        if head:
            self.head = head
        if rel:
            self.rel = rel

#!/usr/bin/python
# -*- coding: UTF-8 -*-


def _get_question_words(words):
    ud_qws = set()
    with open('data/interrogative', 'r', encoding='utf-8') as f:
        for line in f:
            ud_qws.add(line.strip())
    return [(word['term'], word['head']) for word in words if word['pos'] == 'r' and word['term'] in ud_qws]

def get_bowpos(words):
    features = set()
    features.update(['|'.join((word['term'], word['pos'])) for word in words])
    return list(features)


def get_qw(words):
    features = set()
    qws = _get_question_words(words)
    for qw in qws:
        features.add(qw[0])
    return list(features)


def get_rel(words):
    features = set()
    qws = _get_question_words(words)
    for qw in qws:
        rels = [word['term'] for i, word in enumerate(words) if i == qw[1] - 1]
        features.update(rels)
    return list(features)


def get_qwrel(words):
    features = set()
    qws = _get_question_words(words)
    for qw in qws:
        qwrels = ['|'.join((qw[0], word['term'])) for i, word in enumerate(words) if i == qw[1] - 1]
        features.update(qwrels)
    return list(features)



def get_relpos(words):
    features = set()
    qws = _get_question_words(words)
    for qw in qws:
        rels = ['|'.join((word['term'], word['pos'])) for i, word in enumerate(words) if i == qw[1] - 1]
        features.update(rels)
    return list(features)


def get_relne(words):
    features = set()
    qws = _get_question_words(words)
    for qw in qws:
        rels = ['|'.join((word['term'], word['ne'])) for i, word in enumerate(words) if i == qw[1] - 1]
        features.update(rels)
    return list(features)


def get_relposne(words):
    features = set()
    qws = _get_question_words(words)
    for qw in qws:
        rels = ['|'.join((word['term'], word['pos'], word['ne'])) for i, word in enumerate(words) if i == qw[1] - 1]
        features.update(rels)
    return list(features)


def get_qw_rel(words):
    features = set()
    qws = _get_question_words(words)
    for qw in qws:
        rels = [word['term'] for i, word in enumerate(words) if i == qw[1] - 1]
        features.add(qw[0])
        features.update(rels)
    return list(features)


def get_qw_rel_relpos(words):
    features = set()
    qws = _get_question_words(words)
    for qw in qws:
        features.add(qw[0])
        rels = [word for i, word in enumerate(words) if i == qw[1] - 1]
        for rel in rels:
            features.add(rel['term'])
            features.add('|'.join((rel['term'], rel['pos'])))
    return list(features)


def get_qw_rel_relne(words):
    features = set()
    qws = _get_question_words(words)
    for qw in qws:
        features.add(qw[0])
        rels = [word for i, word in enumerate(words) if i == qw[1] - 1]
        for rel in rels:
            features.add(rel['term'])
            features.add('|'.join((rel['term'], rel['ne'])))
    return list(features)


def get_qw_rel_relposne(words):
    features = set()
    qws = _get_question_words(words)
    for qw in qws:
        features.add(qw[0])
        rels = [word for i, word in enumerate(words) if i == qw[1] - 1]
        for rel in rels:
            features.add(rel['term'])
            features.add('|'.join((rel['term'], rel['pos'], rel['ne'])))
    return list(features)


def get_qw_rel_relpos_relne(words):
    features = set()
    qws = _get_question_words(words)
    for qw in qws:
        features.add(qw[0])
        rels = [word for i, word in enumerate(words) if i == qw[1] - 1]
        for rel in rels:
            features.add(rel['term'])
            features.add('|'.join((rel['term'], rel['pos'])))
            features.add('|'.join((rel['term'], rel['ne'])))
    return list(features)


def get_hed(words):
    features = set()
    features.update([word['term'] for word in words if word['rel'] == "HED"])
    return list(features)


def get_sbj(words):
    features = set()
    hed = [(i, word) for i, word in enumerate(words) if word['rel'] == "HED"]
    sbj = [word for word in words if word['rel'] == 'SBV' and word['head']-1 in [index for index, term in hed]]
    features.update([word['term'] for word in sbj])
    return list(features)

def get_obj(words):
    features = set()
    hed = [(i, word) for i, word in enumerate(words) if word['rel'] == "HED"]
    obj = [word for word in words if word['rel'] == 'VOB' and word['head']-1 in [index for index, term in hed]]
    features.update([word['term'] for word in obj])
    return list(features)


def get_hedpos(words):
    features = set()
    features.update(['|'.join((word['term'], word['pos'])) for word in words if word['rel'] == "HED"])
    return list(features)


def get_sbjpos(words):
    features = set()
    hed = [(i, word) for i, word in enumerate(words) if word['rel'] == "HED"]
    sbj = [word for word in words if word['rel'] == 'SBV' and word['head']-1 in [index for index, term in hed]]
    features.update(['|'.join((word['term'], word['pos'])) for word in sbj])
    return list(features)

def get_objpos(words):
    features = set()
    hed = [(i, word) for i, word in enumerate(words) if word['rel'] == "HED"]
    obj = [word for word in words if word['rel'] == 'VOB' and word['head']-1 in [index for index, term in hed]]
    features.update(['|'.join((word['term'], word['pos'])) for word in obj])
    return list(features)


if __name__ == '__main__':
    feature_words = [
        {'term': 'ACLU', 'pos': 'ws', 'ne': 'O', 'head': 3, 'rel': 'ATT'},
        {'term': '的', 'pos': 'u', 'ne': 'O', 'head': 1, 'rel': 'RAD'},
        {'term': '全称', 'pos': 'n', 'ne': 'O', 'head': 4, 'rel': 'SBV'},
        {'term': '是', 'pos': 'v', 'ne': 'O', 'head': 0, 'rel': 'HED'},
        {'term': '什么', 'pos': 'r', 'ne': 'O', 'head': 4, 'rel': 'VOB'}
    ]
    feature_words1 = [
        {'term': '大连', 'pos': 'ns', 'ne': 'B-Ni', 'head': 3, 'rel': 'ATT'},
        {'term': '陆军', 'pos': 'n', 'ne': 'I-Ni', 'head': 3, 'rel': 'ATT'},
        {'term': '学院', 'pos': 'n', 'ne': 'E-Ni', 'head': 5, 'rel': 'ATT'},
        {'term': '的', 'pos': 'u', 'ne': 'O', 'head': 3, 'rel': 'RAD'},
        {'term': '地址', 'pos': 'n', 'ne': 'O', 'head': 6, 'rel': 'SBV'},
        {'term': '是', 'pos': 'v', 'ne': 'O', 'head': 0, 'rel': 'HED'},
        {'term': '什么', 'pos': 'r', 'ne': 'O', 'head': 6, 'rel': 'VOB'}]


    print(get_bow_pos(feature_words))
    print(get_qw(feature_words))
    print(get_rel(feature_words))
    print(get_hed(feature_words))
    print(get_qwrel(feature_words))
    print(get_sbj(feature_words1))
    print(get_obj(feature_words1))
    print(get_rel_pos(feature_words))
    print(get_rel_ne(feature_words))

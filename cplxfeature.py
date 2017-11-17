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


def _coordinate(words, terms):
    for term in terms[:]:
        for index, word in enumerate(words):
            if word['head'] == term[0] and word['rel'] == 'COO':
                terms.append((index+1, word))
                _coordinate(words, [(index+1, word)])


def _continuous(words, kels, rel):
    cons = []
    for kel in kels:
        for index, word in enumerate(words):
            if word['head'] == kel[0] and word['rel'] == rel:
                cons.append((index+1, word))
                cons.extend(_continuous(words, [(index+1, word)], rel))
    return cons


def _hed(words):
    heds = [(index+1, word) for index, word in enumerate(words) if word['rel'] == 'HED']
    _coordinate(words, heds)
    return heds


def get_hed(words):
    features = set()
    heds = _hed(words)
    features.update([word['term'] for i, word in heds])
    return list(features)


def _nearest_sbj(hed, sbjs, max_dist):
    nearest_sbj = None
    for sbj in sbjs:
        dist = abs(sbj[0]-hed[0])
        if dist < max_dist:
            max_dist = dist
            nearest_sbj = sbj
    return nearest_sbj


def _sbj(words):
    sbjs = []
    heds = _hed(words)
    for hed in heds:
        parallel_sbjs = [(index+1, word) for index, word in enumerate(words)
                if word['rel'] == 'SBV' and word['head'] == hed[0]]
        if parallel_sbjs:
            kel_sbj = _nearest_sbj(hed, parallel_sbjs, len(words))
            kel_sbjs = [kel_sbj]
            _coordinate(words, kel_sbjs)
            con_sbjs = _continuous(words, kel_sbjs, 'SBV')
            sbjs.append(kel_sbj)
            sbjs.extend(con_sbjs)
    return sbjs


def get_sbj(words):
    features = set()
    sbjs = _sbj(words)
    features.update([sbj['term'] for index, sbj in sbjs])
    return list(features)


def _farthest_obj(hed, objs, min_dist):
    farthest_obj = None
    for obj in objs:
        dist = abs(obj[0] - hed[0])
        if dist > min_dist:
            min_dist = dist
            farthest_obj = obj
    return farthest_obj


def _obj(words):
    objs = []
    heds = _hed(words)
    for hed in heds:
        parallel_objs = [(index+1, word) for index, word in enumerate(words)
                         if word['rel'] == 'VOB' and word['head'] == hed[0]]
        if parallel_objs:
            kel_obj = _farthest_obj(hed, parallel_objs, 0)
            kel_objs = [kel_obj]
            _coordinate(words, kel_objs)
            con_objs = _continuous(words, kel_objs, 'VOB')
            objs.append(kel_obj)
            objs.extend(con_objs)
    return objs


def get_obj(words):
    features = set()
    objs = _obj(words)
    features.update([word['term'] for index, word in objs])
    return list(features)


def get_hedpos(words):
    features = set()
    heds = _hed(words)
    features.update(['|'.join((word['term'], word['pos'])) for index, word in heds])
    return list(features)


def get_sbjpos(words):
    features = set()
    sbjs = _sbj(words)
    features.update(['|'.join((word['term'], word['pos'])) for index, word in sbjs])
    return list(features)

def get_objpos(words):
    features = set()
    objs = _obj(words)
    features.update(['|'.join((word['term'], word['pos'])) for index, word in objs])
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
        {'term': '在', 'pos': 'p', 'ne': 'O', 'head': 17, 'rel': 'ADV'},
        {'term': '2000年', 'pos': 'nt', 'ne': 'O', 'head': 6, 'rel': 'ATT'},
        {'term': '世界', 'pos': 'n', 'ne': 'O', 'head': 4, 'rel': 'ATT'},
        {'term': '竞争力', 'pos': 'n', 'ne': 'O', 'head': 6, 'rel': 'ATT'},
        {'term': '最新', 'pos': 'a', 'ne': 'O', 'head': 6, 'rel': 'ATT'},
        {'term': '排名', 'pos': 'v', 'ne': 'O', 'head': 7, 'rel': 'ATT'},
        {'term': '中', 'pos': 'nd', 'ne': 'O', 'head': 1, 'rel': 'POB'},
        {'term': '美国', 'pos': 'ns', 'ne': 'S-Ns', 'head': 17, 'rel': 'SBV'},
        {'term': '居', 'pos': 'v', 'ne': 'O', 'head': 17, 'rel': 'SBV'},
        {'term': '第一', 'pos': 'm', 'ne': 'O', 'head': 11, 'rel': 'ATT'},
        {'term': '位', 'pos': 'q', 'ne': 'O', 'head': 12, 'rel': 'SBV'},
        {'term': '排', 'pos': 'v', 'ne': 'O', 'head': 17, 'rel': 'SBV'},
        {'term': '在', 'pos': 'p', 'ne': 'O', 'head': 12, 'rel': 'CMP'},
        {'term': '第二', 'pos': 'm', 'ne': 'O', 'head': 15, 'rel': 'ATT'},
        {'term': '位', 'pos': 'q', 'ne': 'O', 'head': 13, 'rel': 'POB'},
        {'term': '的', 'pos': 'u', 'ne': 'O', 'head': 15, 'rel': 'RAD'},
        {'term': '是', 'pos': 'v', 'ne': 'O', 'head': 0, 'rel': 'HED'},
        {'term': '哪个', 'pos': 'r', 'ne': 'O', 'head': 19, 'rel': 'ATT'},
        {'term': '国家', 'pos': 'n', 'ne': 'O', 'head': 17, 'rel': 'VOB'},
        {'term': 'fakeSBJ', 'pos': 'f', 'ne': 'O', 'head': 12, 'rel': 'COO'},
        {'term': 'fakeHED', 'pos': 'f', 'ne': 'O', 'head': 17, 'rel': 'COO'}
    ]
    feature_words2 = [
        {'term': '谁', 'pos': 'r', 'ne': 'O', 'head': 2, 'rel': 'SBV'},
        {'term': '发现', 'pos': 'v', 'ne': 'O', 'head': 0, 'rel': 'HED'},
        {'term': '了', 'pos': 'u', 'ne': 'O', 'head': 2, 'rel': 'RAD'},
        {'term': '白光', 'pos': 'n', 'ne': 'O', 'head': 5, 'rel': 'SBV'},
        {'term': '是', 'pos': 'v', 'ne': 'O', 'head': 2, 'rel': 'VOB'},
        {'term': '七色光', 'pos': 'nz', 'ne': 'O', 'head': 7, 'rel': 'SBV'},
        {'term': '组成', 'pos': 'v', 'ne': 'O', 'head': 5, 'rel': 'VOB'},
        {'term': '的', 'pos': 'u', 'ne': 'O', 'head': 7, 'rel': 'RAD'},
        {'term': 'fack', 'pos': 'f', 'ne': 'O', 'head': 2, 'rel': 'IC'}
    ]
    feature_words3 = [
        {'term': '我', 'pos': 'r', 'ne': 'O', 'head': 2, 'rel': 'SBV'},
        {'term': '爱', 'pos': 'v', 'ne': 'O', 'head': 0, 'rel': 'HED'},
        {'term': '你', 'pos': 'r', 'ne': 'O', 'head': 2, 'rel': 'VOB'},
        {'term': '用', 'pos': 'p', 'ne': 'O', 'head': 7, 'rel': 'ADV'},
        {'term': '英语', 'pos': 'nz', 'ne': 'O', 'head': 4, 'rel': 'POB'},
        {'term': '怎么', 'pos': 'r', 'ne': 'O', 'head': 7, 'rel': 'ADV'},
        {'term': '说', 'pos': 'v', 'ne': 'O', 'head': 2, 'rel': 'COO'}
    ]







    print(get_qw(feature_words1))
    print(get_rel(feature_words1))
    print(get_hed(feature_words1))
    print(get_sbj(feature_words1))
    print(get_obj(feature_words1))
    print(get_hedpos(feature_words1))
    print(get_sbjpos(feature_words1))
    print(get_objpos(feature_words1))


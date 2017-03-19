#!/usr/bin/env python
# coding: utf-8

from datetime import date
import os
import re


def serialize_bag_jag(tpl):
    from BM25F.exp import bag_dict
    from BM25F.exp import bag_jag
    import BM25F.ja
    sf = BM25F.ja.StemFilter()
    pf = BM25F.ja.PosFilter()
    tokenizer = BM25F.ja.Tokenizer(sf, pf)
    bj = bag_jag()
    query_id, dicts, dir_path = tpl
    for d in dicts:
        bd = bag_dict()
        bd.read(tokenizer, d)
        bj.append(bd)
    bj.write(os.path.join(dir_path, query_id + '.txt'))


class ClickThrough(dict):
    keys = [
        'query_id',
        'question_id',
        'mode_rank',
        'ctr',
        'male',
        'female',
        '10-',
        '10s',
        '20s',
        '30s',
        '40s',
        '50s',
        '60+',
    ]
    key2iid = {
        'male': '1',
        'female': '2',
        '10-': '3',
        '10s': '4',
        '20s': '5',
        '30s': '6',
        '40s': '7',
        '50s': '8',
        '60+': '9',
    }
    separator = '\t'

    def __missing__(self, query_id):
        self[query_id] = {}
        return self[query_id]

    def to_pagebias(self, count_floor=100, base=10):
        rank2count = [0] * 1001
        for qid, remainder in self.items():
            for did, d in remainder.items():
                rank = int(d['mode_rank'])
                rank2count[rank] += 1
        result = []
        rank = 1
        while rank < 1001 and count_floor <= rank2count[rank]:
            result.append(rank2count[rank])
            rank += base
        if 0 < len(result) and 0 < result[0]:
            baseline = result[0]
            result = [raw / baseline for raw in result]
        return result

    def to_rankbias(self, count_floor=1000):
        rank2ctrs = {}
        for qid, remainder in self.items():
            for did, d in remainder.items():
                rank = int(d['mode_rank'])
                if rank not in rank2ctrs:
                    rank2ctrs[rank] = []
                rank2ctrs[rank].append(float(d['ctr']))
        result = []
        rank = 1
        while rank in rank2ctrs and count_floor <= len(rank2ctrs[rank]):
            ctrs = rank2ctrs[rank]
            result.append(sum(ctrs) / len(ctrs))
            rank += 1
        if 0 < len(result) and 0 < result[0]:
            baseline = result[0]
            result = [raw / baseline for raw in result]
        return result

    def read(self, path, expected_count=440163):
        from sys import stderr
        head = 'ClickThrough::read'
        count = 0
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                count += 1
                if count % 40000 == 0:
                    stderr.write('%s is at line %i\n' % (head, count))
                d = {}
                l = line.rstrip().split(ClickThrough.separator)
                try:
                    for i, key in enumerate(ClickThrough.keys):
                        d[key] = l[i]
                except IndexError:
                    stderr.write('%s: IndexError at line %i\n' % (head, count))
                    continue
                self[d['query_id']][d['question_id']] = d
        if expected_count is not None:
            assert count == expected_count
        return self

    def to_relevance(self):
        from TREC import Relevance
        result = Relevance()
        for qid, remainder in self.items():
            for did, d in remainder.items():
                for key in ClickThrough.keys[4:]:
                    v = float(d[key]) * float(d['ctr'])
                    if 0 < v:
                        if v <= 0.25:
                            v = 1
                        elif v <= 0.5:
                            v = 2
                        elif v <= 0.75:
                            v = 3
                        else:
                            v = 4
                        result[qid][ClickThrough.key2iid[key]][did] = v
        return result


class Query(dict):
    linebreak = '\n'
    separator = '\t'

    def read(self, path):
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                query_id, query = line.split(Query.separator, 1)
                query = query.rstrip()
                self[query_id] = query
        return self

    def write(self, path):
        with open(path, 'w', encoding='utf-8') as file:
            for k in sorted(list(self.keys())):
                file.write(Query.separator.join([k, self[k]]))
                file.write(Query.linebreak)
        return self

    def tokenize(self):
        from BM25F.ja import PosFilter
        from BM25F.ja import StemFilter
        from BM25F.ja import Tokenizer
        from BM25F.exp import bag_of_words
        result, tokenizer = {}, Tokenizer(StemFilter(), PosFilter())
        for qid, q in self.items():
            result[qid] = bag_of_words().read(tokenizer, q)
        return result


class QuestionData(dict):
    keys = [
        'query_id',
        'rank',
        'question_id',
        'title',
        'snippets',
        'status',
        'timestamp',
        'answer_count',
        'view_count',
        'category',
        'question_body',
        'best_answer_body',
    ]
    separator = '\t'

    def __missing__(self, query_id):
        self[query_id] = []
        return self[query_id]

    def format(self):
        def parse_date(s):
            s = s.split(' ')[0]
            l = s.split('/', 2)
            return date(*[int(t) for t in l])
        epoch = parse_date('2016/12/12 00:00:00')
        for query_id, dicts in self.items():
            for d in dicts:
                d.pop('query_id')
                d['~rank'] = int(d.pop('rank'))
                d['_question_id'] = d.pop('question_id')
                d['~status'] = {
                    '解決受付中': 0,
                    '投票受付中': 1,
                    '解決済み': 2,
                }[d.pop('status')]
                days_passed = (epoch - parse_date(d.pop('timestamp'))).days
                d['~days_passed'] = days_passed
                d['~answer_count'] = int(d.pop('answer_count'))
                d['~view_count'] = int(d.pop('view_count'))
        return self

    def read(self, path, expected_count=1967274):
        from sys import stderr
        head = 'QuestionData::read'
        count = 0
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                count += 1
                if count % 200000 == 0:
                    stderr.write('%s is at line %i\n' % (head, count))
                d = {}
                l = line.rstrip('\n').split(QuestionData.separator)
                try:
                    for i, key in enumerate(QuestionData.keys):
                        d[key] = l[i]
                except IndexError:
                    stderr.write('%s: IndexError at line %i\n' % (head, count))
                    continue
                self[d['query_id']].append(d)
        if expected_count is not None:
            assert count == expected_count
        return self

    def write_bag_jags(self, dir_path):
        import multiprocessing as mp
        dir_path = dir_path.rstrip(os.path.sep)
        self.format()
        buffer = [pair + (dir_path,) for pair in self.items()]
        mp.Pool(mp.cpu_count() - 1).map(serialize_bag_jag, buffer)


class Run(dict):
    linebreak = '\n'
    separator = '\t'

    def __missing__(self, query_id):
        self[query_id] = []
        return self[query_id]

    def read(self, path):
        def r(line):
            line = re.sub(r'\r?\n$', '', line)
            query_id, document_id = line.split(Run.separator, 1)
            self[query_id].append(document_id)
        with open(path, 'r') as file:
            first_line = file.readline()
            if re.match(r'OLQ-\d+\s+q\d+\r?\n', first_line):  # No description
                r(first_line)
            else:  # Skip description
                print(first_line)
                pass
            for line in file.readlines():
                r(line)
        return self

    def write(self, path):
        with open(path, 'w') as file:
            for query_id in sorted(list(self.keys())):
                document_ids = self[query_id]
                for document_id in document_ids:
                    line = Run.separator.join([query_id, document_id])
                    file.write(line)
                    file.write(Run.linebreak)
        return self

#!/usr/bin/env python
# coding: utf-8


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
    separator = '\t'

    def __missing__(self, query_id):
        self[query_id] = {}
        return self[query_id]

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


class Run(dict):
    linebreak = '\n'
    separator = '\t'

    def __missing__(self, query_id):
        self[query_id] = []
        return self[query_id]

    def read(self, path):
        with open(path, 'r') as file:
            for line in file:
                query_id, document_id = line.split(Run.separator, 1)
                document_id = document_id.rstrip()
                self[query_id].append(document_id)
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

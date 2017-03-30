#!/usr/bin/env python
# coding: utf-8

from LETOR import Relevance as OriginalRelevance
import re


class Relevance(OriginalRelevance):

    class relevance(int):

        def __eq__(self, other):
            return (
                super() and
                self.iqid == other.iqid and
                self.feature == other.feature
            )

        def __new__(self, value, iqid, feature):
            self = int.__new__(self, value)
            self.iqid = iqid
            self.feature = feature
            return self

    def read(self, path):
        with open(path, 'r') as file:
            for line in file:
                body, meta = line.split('#')
                value, remainder = re.split(r'\s+', body, 1)
                value = int(value)
                iqid, remainder = re.split(r'\s+', remainder, 1)
                iqid = int(iqid.split(':')[-1])
                remainder = re.split(r'\s+', remainder.strip())
                feature = {}
                for token in remainder:
                    k, v = token.split(':')
                    feature[int(k)] = float(v)
                qid, did = re.split(r'\s+', meta.strip(), 1)
                self[qid]['0'][did] = Relevance.relevance(value, iqid, feature)
        return self

    def write(self, path):
        with open(path, 'w') as file:
            for qid in sorted(self.keys()):
                remainder = self[qid]
                for docid in sorted(remainder['0'].keys()):
                    rel = remainder['0'][docid]
                    iqid = rel.iqid
                    feature = rel.feature
                    file.write(str(rel) + ' ')
                    file.write('qid:%i ' % iqid)
                    for k in sorted(feature.keys()):
                        file.write(str(k) + ':')
                        file.write(str(feature[k]) + ' ')
                    file.write('# %s %s\n' % (qid, docid))
        return self


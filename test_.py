#!/usr/bin/env python
# coding: utf-8

import OpenLiveQ
import unittest


class TestOpenLiveQ(unittest.TestCase):

    def test_clickthrough(self):
        source = OpenLiveQ.ClickThrough()
        source.read('./sample_clickthrough.tsv', 1)
        self.assertEqual(source, {
            '2345': {
                'q90123456789': dict(zip(OpenLiveQ.ClickThrough.keys, [
                    'OLQ-2345',
                    'q90123456789',
                    '123',
                    '1.000',
                    '0.200',
                    '0.800',
                    '0.400',
                    '0.600',
                    '0.000',
                    '0.000',
                    '0.000',
                    '0.000',
                    '0.000',
                ])),
            },
        })

    def test_clickthrough_to_pagebias(self):
        source = OpenLiveQ.ClickThrough()
        source.read('./sample_clickthrough_long.tsv', 10)
        expect = [1.0, 0.5]
        actual = source.to_pagebias(count_floor=2, base=2)
        for e, a in zip(expect, actual):
            self.assertTrue(-0.000001 < e - a < 0.000001)

    def test_clickthrough_to_rankbias(self):
        source = OpenLiveQ.ClickThrough()
        source.read('./sample_clickthrough_long.tsv', 10)
        expect = [1.0, 0.933333, 0.8]
        actual = source.to_rankbias(count_floor=2)
        for e, a in zip(expect, actual):
            self.assertTrue(-0.000001 < e - a < 0.000001)

    def test_clickthrough_to_relevance(self):
        source = OpenLiveQ.ClickThrough()
        source.read('./sample_clickthrough.tsv', 1)
        qid, did = '2345', 'q90123456789'
        expect = {
            qid: {
                '1': {did: 1},
                '2': {did: 4},
                '3': {did: 2},
                '4': {did: 3},
            },
        }
        actual = source.to_relevance()
        print(actual)
        self.assertEqual(expect, actual)

    def test_query(self):
        source = OpenLiveQ.Query().read('./sample_query.tsv')
        source.write('./tmp_query.tsv')
        destination = OpenLiveQ.Query().read('./tmp_query.tsv')
        self.assertEqual(source, destination)

    def test_questiondata(self):
        source = OpenLiveQ.QuestionData()
        source.read('./sample_questiondata.tsv', 1)
        self.assertEqual(source, {
            '2345': [
                dict(zip(OpenLiveQ.QuestionData.keys, [
                    'OLQ-2345',
                    '123',
                    'q90123456789',
                    'タイトル',
                    'スニペット',
                    '解決済み',
                    '2016/11/13 03:35:34',
                    '1',
                    '42',
                    '大カテゴリ > 小カテゴリ',
                    '質問本文',
                    'ベストアンサー本文',
                ])),
            ],
        })

    def test_run(self):
        source = OpenLiveQ.Run().read('./sample_run.tsv')
        source.write('./tmp_run.tsv')
        destination = OpenLiveQ.Run().read('./tmp_run.tsv')
        self.assertEqual(source, destination)


if __name__ == '__main__':
    unittest.main()

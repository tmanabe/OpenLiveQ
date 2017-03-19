#!/usr/bin/env python
# coding: utf-8

from BM25F.exp import bag_jag
import OpenLiveQ
import tempfile
import unittest


class TestOpenLiveQ(unittest.TestCase):

    def test_clickthrough(self):
        source = OpenLiveQ.ClickThrough()
        source.read('./sample_clickthrough.tsv', 1)
        self.assertEqual(source, {
            'OLQ-2345': {
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
        qid, did = 'OLQ-2345', 'q90123456789'
        expect = {
            qid: {
                '1': {did: 1},
                '2': {did: 4},
                '3': {did: 2},
                '4': {did: 3},
            },
        }
        actual = source.to_relevance()
        self.assertEqual(expect, actual)

    def test_query(self):
        source = OpenLiveQ.Query().read('./sample_query.tsv')
        d = tempfile.TemporaryDirectory()
        p = '%s/tmp_query.tsv' % d.name
        source.write(p)
        destination = OpenLiveQ.Query().read(p)
        d.cleanup()
        self.assertEqual(source, destination)

    def test_questiondata(self):
        source = OpenLiveQ.QuestionData()
        source.read('./sample_questiondata.tsv', 1)
        self.assertEqual(source, {
            'OLQ-2345': [
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

    def test_questiondata_format(self):
        source = OpenLiveQ.QuestionData()
        source.read('./sample_questiondata.tsv', 1)
        self.assertEqual(source.format(), {
            'OLQ-2345': [
                {
                    '~rank': 123,
                    '_question_id': 'q90123456789',
                    'title': 'タイトル',
                    'snippets': 'スニペット',
                    '~status': 2,
                    '~days_passed': 29,
                    '~answer_count': 1,
                    '~view_count': 42,
                    'category': '大カテゴリ > 小カテゴリ',
                    'question_body': '質問本文',
                    'best_answer_body': 'ベストアンサー本文',
                },
            ],
        })

    def test_questiondata_write(self):
        source = OpenLiveQ.QuestionData()
        source.read('./sample_questiondata.tsv', 1)
        d = tempfile.TemporaryDirectory()
        p = '%s/OLQ-2345.txt' % d.name
        source.write_bag_jags(d.name)
        expect = bag_jag().read('./sample_serialized_bag_jag.txt')
        actual = bag_jag().read(p)
        d.cleanup()
        self.assertEqual(expect.body, actual.body)
        self.assertEqual(expect.df, actual.df)
        self.assertEqual(expect.total_len, actual.total_len)

    def test_run(self):
        source = OpenLiveQ.Run().read('./sample_run.tsv')
        d = tempfile.TemporaryDirectory()
        p = '%s/tmp_run.tsv' % d.name
        source.write(p)
        destination = OpenLiveQ.Run().read(p)
        d.cleanup()
        self.assertEqual(source, destination)


if __name__ == '__main__':
    unittest.main()

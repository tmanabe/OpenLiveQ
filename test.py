#!/usr/bin/env python
# coding: utf-8

import OpenLiveQ
import unittest


class TestOpenLiveQ(unittest.TestCase):

    def test_query(self):
        source = OpenLiveQ.Query().read('./sample_query.txt')
        source.write('./tmp_query.txt')
        destination = OpenLiveQ.Query().read('./tmp_query.txt')
        self.assertEqual(source, destination)

    def test_run(self):
        source = OpenLiveQ.Run().read('./sample_run.txt')
        source.write('./tmp_run.txt')
        destination = OpenLiveQ.Run().read('./tmp_run.txt')
        self.assertEqual(source, destination)


if __name__ == '__main__':
    unittest.main()

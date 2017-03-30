#!/usr/bin/env python
# coding: utf-8

from OpenLiveQ_addon import Relevance
import tempfile
import unittest


class TestOpenLiveQ_addon(unittest.TestCase):

    def test_relevance(self):
        source = Relevance()
        source.read('./sample_relevance.txt')
        d = tempfile.TemporaryDirectory()
        p = '%s/tmp_relevance.txt' % d.name
        source.write(p)
        destination = Relevance()
        destination.read(p)
        d.cleanup()
        self.assertEqual(source, destination)

    def test_update(self):
        source = Relevance()
        source.read('./sample_relevance.txt')
        d = tempfile.TemporaryDirectory()
        p = '%s/tmp_relevance.txt' % d.name
        source.update(source)
        source.write(p)
        expected = Relevance()
        expected.read('./sample_relevance2.txt')
        actual = Relevance()
        actual.read(p)
        d.cleanup()
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()

#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Author: Rajat Gupta
Description:
"""

import unittest

from samantha import __version__, __project_name__


class TestSample(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_0000_test_list_assertion(self):
        self.assertEqual(200, 200)

    def test_0001_test_version(self):
        self.assertGreaterEqual(__version__.__version__, '0.0.1')

    def test_0001_test_project_name(self):
        self.assertEquals(__project_name__.__project_name__, 'samantha')


def suite():
    "Test suite"
    test_suite = unittest.TestSuite()
    test_suite.addTests(
        unittest.TestLoader().loadTestsFromTestCase(TestSample)
    )
    return test_suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

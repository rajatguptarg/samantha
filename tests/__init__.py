#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Author: Rajat Gupta
Description:
"""

import unittest
from .test_sample import TestSample
from .test_entities import TestEntity


def suite():
    """
    Define suite
    """
    test_suite = unittest.TestSuite()
    test_suite.addTests([
        unittest.TestLoader().loadTestsFromTestCase(TestSample),
        unittest.TestLoader().loadTestsFromTestCase(TestEntity),
    ])
    return test_suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

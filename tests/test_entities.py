#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Author: Rajat Gupta
Description:
"""

import unittest

from samantha import entities


class TestEntity(unittest.TestCase):
    def setUp(self):
        self.d = {"name": "samantha", "profile": {"age": 20, "admin": [True]}}

    def tearDown(self):
        pass

    def test_0000_create_object_from_dict(self):
        obj = entities.dict_to_object(self.d)
        self.assertEqual(obj.name, 'samantha')

    def test_0001_check_profile_object(self):
        obj = entities.dict_to_object(self.d)
        self.assertEqual(obj.profile.age, 20)
        self.assertEqual(obj.profile.admin, [True])


def suite():
    "Test suite"
    test_suite = unittest.TestSuite()
    test_suite.addTests(
        unittest.TestLoader().loadTestsFromTestCase(TestEntity)
    )
    return test_suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

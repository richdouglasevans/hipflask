# -*- coding: utf-8 -*-

import unittest

from hipflask import ContentNegotiatingResponsifier


class ContentNegotiatingResponsifierTests(unittest.TestCase):
    def test_ctor_with_none_responsifiers(self):
        with self.assertRaises(AssertionError):
            ContentNegotiatingResponsifier(None)

    def test_ctor_with_empty_responsifiers_mapping(self):
        with self.assertRaises(AssertionError):
            ContentNegotiatingResponsifier(dict())

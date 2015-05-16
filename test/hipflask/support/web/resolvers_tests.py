# -*- coding: utf-8 -*-

import unittest

from hamcrest import *
from hipflask.support.web.resolvers import *


class SimpleSuffixBasedViewResolverTests(unittest.TestCase):
    def test_ctor_with_defaults(self):
        SimpleSuffixBasedViewResolver()

    def test_ctor_with_custom_suffix(self):
        SimpleSuffixBasedViewResolver(suffix='.txt')

    def test_ctor_with_none_suffix(self):
        with self.assertRaises(AssertionError):
            SimpleSuffixBasedViewResolver(suffix=None)

    def test_ctor_with_empty_suffix(self):
        with self.assertRaises(AssertionError):
            SimpleSuffixBasedViewResolver(suffix='')

    def test_ctor_with_whitespace_suffix(self):
        with self.assertRaises(AssertionError):
            SimpleSuffixBasedViewResolver(suffix='  ')

    def test_ctor_with_none_view_name_key(self):
        with self.assertRaises(AssertionError):
            SimpleSuffixBasedViewResolver(view_name_key=None)

    def test_ctor_with_empty_view_name_key(self):
        with self.assertRaises(AssertionError):
            SimpleSuffixBasedViewResolver(view_name_key='')

    def test_ctor_with_whitespace_view_name_key(self):
        with self.assertRaises(AssertionError):
            SimpleSuffixBasedViewResolver(view_name_key='  ')

    def test_resolve_view_with_defaults(self):
        logical_view_name = 'login'

        resolver = SimpleSuffixBasedViewResolver()
        view_name = resolver.resolve_view(view_name=logical_view_name)
        assert_that(view_name, is_('login.html'))

    def test_resolve_view_with_custom_suffix(self):
        logical_view_name = 'login'

        resolver = SimpleSuffixBasedViewResolver(suffix='.txt')
        view_name = resolver.resolve_view(view_name=logical_view_name)
        assert_that(view_name, is_('login.txt'))

    def test_resolve_view_with_custom_suffix_and_custom_view_name_key(self):
        logical_view_name = 'login'

        resolver = SimpleSuffixBasedViewResolver(suffix='.txt', view_name_key='logical_view')
        view_name = resolver.resolve_view(logical_view=logical_view_name)
        assert_that(view_name, is_('login.txt'))

    def test_resolve_view_with_missing_logical_view_name(self):
        with self.assertRaises(CannotFindViewException):
            resolver = SimpleSuffixBasedViewResolver()
            resolver.resolve_view(missing=None)

    def test_resolve_view_with_none_logical_view_name(self):
        with self.assertRaises(CannotFindViewException):
            resolver = SimpleSuffixBasedViewResolver()
            resolver.resolve_view(view_name=None)


class SimpleMappingBasedViewResolverTests(unittest.TestCase):
    def test_ctor_with_none_view_mappings(self):
        with self.assertRaises(AssertionError):
            SimpleMappingBasedViewResolver(None)

    def test_ctor_with_empty_view_mappings(self):
        with self.assertRaises(AssertionError):
            SimpleMappingBasedViewResolver(dict())

    def test_resolve_view_sunny_day(self):
        resolver = SimpleMappingBasedViewResolver(dict(foo='bar'))
        view_name = resolver.resolve_view(view_name='foo')
        assert_that(view_name, is_('bar'))

    def test_resolve_view_missing(self):
        with self.assertRaises(CannotFindViewException):
            resolver = SimpleMappingBasedViewResolver(dict(foo='bar'))
            resolver.resolve_view(view_name='not_here')

    def test_resolve_view_empty(self):
        with self.assertRaises(CannotFindViewException):
            resolver = SimpleMappingBasedViewResolver(dict(foo=''))
            resolver.resolve_view(view_name='foo')

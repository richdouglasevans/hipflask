# -*- coding: utf-8 -*-

import unittest

from hamcrest import *
from hipflask import HipflaskException
from hipflask.support.strings import safe_string, is_stringy, has_text, message_from


# noinspection PyPep8Naming
from hipflask.support.strings import UnknownEncodingException


class StringsTests(unittest.TestCase):
    def test_is_stringy_with_string(self):
        self.assertTrue(is_stringy(''))

    def test_is_stringy_with_unicode(self):
        self.assertTrue(is_stringy(u''))

    def test_is_stringy_with_none(self):
        self.assertFalse(is_stringy(None))

    def test_is_stringy_with_other_object(self):
        self.assertFalse(is_stringy([]))

    def test_safe_string_with_regular_string(self):
        expected_value = 'There Can Be Only One'
        value = safe_string(expected_value)
        self.assertEqual(expected_value, value)

    def test_safe_string_with_regular_string_does_trim_whitespace(self):
        expected_value = 'There Can Be Only One'
        value = safe_string('   {} \t   '.format(expected_value))
        self.assertEqual(expected_value, value)

    def test_safe_string_with_none(self):
        expected_value = ''
        value = safe_string(None)
        self.assertEqual(expected_value, value)

    def test_safe_string_with_bogus_encoding(self):
        self.assertRaises(UnknownEncodingException,
                          lambda: safe_string('whatever', 'Not an encoding.'))

    def test_has_text_with_none(self):
        self.assertFalse(has_text(None))

    def test_has_text_with_empty_string(self):
        self.assertFalse(has_text(''))

    def test_has_text_with_empty_unicode_string(self):
        self.assertFalse(has_text(u''))

    def test_has_text_with_unicode_string_filled_with_just_whitespace(self):
        self.assertFalse(has_text(u'    '))

    def test_has_text_with_string_filled_with_just_whitespace(self):
        self.assertFalse(has_text('\t    '))

    def test_has_text_with_not_empty_string(self):
        self.assertTrue(has_text('a'))

    def test_has_text_with_not_empty_unicode_string(self):
        self.assertTrue(has_text(u'a   '))
        self.assertTrue(has_text('a'))

    def test_message_from_sunny_day(self):
        expected_message = 'hi'
        ex = HipflaskException(expected_message)
        message = message_from(ex)
        assert_that(message, is_(expected_message))

    def test_message_from_two_levels_deep(self):
        expected_message = 'hi'
        ex = HipflaskException(HipflaskException(expected_message))
        message = message_from(ex)
        assert_that(message, is_(expected_message))

# -*- coding: utf-8 -*-

import unittest

from hamcrest import *
from hipflask.support import IdBased, NameToWithSimpleNameMapper, WithSimpleNameToNameMapper, WithSimpleName, \
    CodedError, CodedErrors, FieldError
from hipflask.support.functions import identity


class IdBasedTests(unittest.TestCase):
    def test_is_transient_from_the_off(self):
        obj = IdBased()

        self.assertTrue(obj.is_transient())
        self.assertFalse(obj.is_persistent())

    def test_is_persistent(self):
        obj = IdBased(id=12)

        self.assertFalse(obj.is_transient())
        self.assertTrue(obj.is_persistent())


class NameToWithSimpleNameMapperTests(unittest.TestCase):
    def test_sunny_day(self):
        name = 'Shirley Valentine'
        value = NameToWithSimpleNameMapper(identity).map(name)

        self.assertEqual(name, value)

    def test_ctor_chokes_when_given_no_creator_function(self):
        self.assertRaises(AssertionError, NameToWithSimpleNameMapper, None)


class WithSimpleNameToNameMapperTests(unittest.TestCase):
    def test_sunny_day(self):
        name = 'Shirley Valentine'
        wsm = WithSimpleName(name)
        value = WithSimpleNameToNameMapper().map(wsm)

        self.assertEqual(name, value)


class CodedErrorTests(unittest.TestCase):
    def test_equal_with_equal_instances(self):
        one = CodedError(1, message='one')
        one_ = CodedError(1, message='one')

        self.assertEqual(one, one_)

    def test_equal_with_same_instance(self):
        one = CodedError(1, message='one')

        self.assertEqual(one, one)

    def test_equal_with_unequal_instances(self):
        one = CodedError(1, message='one')
        two = CodedError(2, message='two')

        self.assertNotEqual(one, two)

    def test_equal_with_unequal_instances_of_differing_types(self):
        one = CodedError(1, message='one')
        two = 'ohilovearainynight'

        self.assertNotEqual(one, two)

    def test_equal_with_unequal_instances_of_none(self):
        one = CodedError(1, message='one')
        two = None

        self.assertNotEqual(one, two)


class CodedErrorsTests(unittest.TestCase):
    def test_ctor_empty(self):
        errors = CodedErrors()

        self.assertFalse(errors.contains_errors())
        self.assertEqual(0, errors.length)

    def test_add_field_error(self):
        error = CodedError(1, message='one')
        errors = CodedErrors().add_field_error(FieldError('name', error))

        assert_that(errors, not_none())
        self.assertTrue(errors.contains_errors())
        self.assertEqual(1, errors.length)

        field_errors = errors.field_errors
        assert_that(field_errors, not_none())
        self.assertEqual(1, len(field_errors))
        self.assertEqual(error, field_errors[0].error)

    def test_add_global_error(self):
        error = CodedError(1, message='one')
        errors = CodedErrors().add_global_error(error)

        assert_that(errors, not_none())
        self.assertTrue(errors.contains_errors())
        self.assertEqual(1, errors.length)

        global_errors = errors.global_errors
        assert_that(global_errors, not_none())
        self.assertEqual(1, len(global_errors))
        self.assertEqual(error, global_errors[0])

    def test_add_mix_of_field_and_global_errors(self):
        error = CodedError(1, message='one')
        errors = CodedErrors().add_field_error(FieldError('name', error)).add_global_error(error)

        assert_that(errors, not_none())
        self.assertTrue(errors.contains_errors())
        self.assertTrue(errors.has_field_errors())
        self.assertTrue(errors.has_global_errors())
        self.assertEqual(2, errors.length)

        field_errors = errors.field_errors
        assert_that(field_errors, not_none())
        self.assertEqual(1, len(field_errors))
        self.assertEqual(error, field_errors[0].error)

        global_errors = errors.global_errors
        assert_that(global_errors, not_none())
        self.assertEqual(1, len(global_errors))
        self.assertEqual(error, global_errors[0])

    def test_has_field_errors_for(self):
        error = CodedError(1, message='one')
        errors = CodedErrors().add_field_error(FieldError('name', error))

        self.assertTrue(errors.has_field_errors_for('name'))

    def test_has_field_errors_for_rainy_day(self):
        error = CodedError(1, message='one')
        errors = CodedErrors().add_field_error(FieldError('name', error))

        self.assertFalse(errors.has_field_errors_for('rhubarbisgreatonaspringday'))

    def test_field_errors_for_scalar(self):
        error = CodedError(1, message='one')
        errors = CodedErrors().add_field_error(FieldError('name', error))

        name_errors = errors.field_errors_for('name')

        assert_that(name_errors, not_none())
        self.assertEqual(1, len(name_errors))

    def test_field_errors_for_multiple(self):
        first = FieldError('name', CodedError(1, message='first'))
        second = FieldError('name', CodedError(1, message='second'))
        errors = CodedErrors().add_field_error(first).add_field_error(second)

        name_errors = errors.field_errors_for('name')

        assert_that(name_errors, not_none())
        self.assertEqual(2, len(name_errors))
        self.assertEqual(first, name_errors[0])
        self.assertEqual(second, name_errors[1])

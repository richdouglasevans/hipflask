# -*- coding: utf-8 -*-

import logging

from hipflask.support.strings import safe_string, has_text


DEVELOPMENT = 'DEVELOPMENT'
PRODUCTION = 'PRODUCTION'
TEST = 'TEST'


def is_production(name):
    return PRODUCTION == name


def is_development(name):
    return DEVELOPMENT == name


def is_test(name):
    return TEST == name


def is_debug_mode(app):
    return app.config.get('DEBUG', False)


class HipflaskException(Exception):
    """
    Base application exception class.
    """

    def __init__(self, message, cause=None):
        super(HipflaskException, self).__init__()

        self.message = message
        self.cause = cause

    def __str__(self):
        return '{} "{}"'.format(self.__class__.__name__, self.message)


class IdBased(object):
    """
    A mixin for classes that support an ID value.
    """

    # noinspection PyShadowingBuiltins,PyUnusedLocal
    def __init__(self, id=None, *args, **kwargs):
        self._id = id

    @property
    def id(self):
        """
        Return the persistent identity value.

        Will be L{None} if this instance is transient.
        """

        return self._id

    def is_persistent(self):
        """
        Is this instance persistent?

        An ID value that is not L{None} indicates persistence.

        @return: C{True} iff this class is persistent.
        """

        return self._id is not None

    def is_transient(self):
        """
        Is this instance transient?

        An ID value that is L{None} indicates transience.

        @return: C{True} iff this class is transient.
        """

        return not self.is_persistent()


class WithSimpleName(object):
    """
    A mixin for classes with a name field.
    """

    def __init__(self, name):
        super(WithSimpleName, self).__init__()
        assert has_text(name), 'The name is required.'

        self.name = safe_string(name)

    def __eq__(self, other):
        if type(other) is type(self):
            return self.name == other.name
        else:
            return False


class WithSimpleNameToNameMapper(object):
    @staticmethod
    def map(with_simple):
        return with_simple.name


class NameToWithSimpleNameMapper(object):
    def __init__(self, creator):
        assert creator, 'The creator function is required.'

        self.creator = creator

    def map(self, name):
        return self.creator(name)


class CodedError(IdBased):
    """
    An error that has both a code and a message.

    The code is useful in deriving localized error messages.

    The message is intended as a default description, to be used when there is
    no localised error message.
    """

    def __init__(self, code, message=None, **kwargs):
        super(CodedError, self).__init__(**kwargs)

        self.code = code
        self.message = safe_string(message)

    def __str__(self):
        return '{} [{}, "{}"]'.format(self.__class__.__name__, self.code, self.message)

    def __eq__(self, other):
        if type(other) is type(self):
            return self.code == other.code and self.message == other.message
        else:
            return False

    def with_message(self, message):
        """
        Build a new C{CodedError} customised with the supplied C{message}.

        @param message: the message; can be C{None}.
        @return: a new C{CodedError}; never C{None}.
        """

        return CodedError(self.code, message=message)


class FieldError(object):
    def __init__(self, field_name, error):
        super(FieldError, self).__init__()

        assert has_text(field_name), 'The field name is required.'
        assert error is not None, 'The error is required.'

        self.field_name = safe_string(field_name)
        self.error = error

    def __str__(self):
        return '{} ["{}"={}]'.format(self.__class__.__name__, self.field_name, self.error)

    def __eq__(self, other):
        if type(other) is type(self):
            return self.field_name == other.field_name and self.error == other.error
        else:
            return False

    @property
    def code(self):
        return self.error.code

    @property
    def message(self):
        return self.error.message


class CodedErrors(object):
    """
    A collection of C{CodedError} instances.

    We use this as opposed to a list of such errors because this is aware of
    the distinction between a "global" error--an error that applies to a
    resource as whole or to a scope bigger than a single resource--and a
    "field" error--an error that applies at the level of a single resource or
    field.
    """

    def __init__(self):
        super(CodedErrors, self).__init__()

        self.errors = []

    def contains_errors(self):
        return len(self.errors) > 0

    @property
    def length(self):
        return len(self.errors)

    @property
    def field_errors(self):
        return filter(lambda error: isinstance(error, FieldError), self.errors)

    def has_field_errors(self):
        return len(self.field_errors) > 0

    @property
    def global_errors(self):
        return filter(lambda error: isinstance(error, CodedError), self.errors)

    def has_global_errors(self):
        return len(self.global_errors) > 0

    def add_field_error(self, field_error):
        assert field_error is not None, 'The field error is required.'

        self.errors.append(field_error)
        return self

    def add_global_error(self, global_error):
        assert global_error is not None, 'The global error is required.'

        self.errors.append(global_error)
        return self

    def field_errors_for(self, field_name):
        return filter(lambda error: error.field_name == field_name, self.field_errors)

    def has_field_errors_for(self, field_name):
        errors = self.field_errors_for(field_name)
        return len(errors) > 0

    def __str__(self):
        return '{} [{} errors]'.format(self.__class__.__name__, len(self.errors))


ERROR_SERVER_ERROR = CodedError(3, message='Gosh, something rather unexpected went wrong.')


def logger_for(instance):
    """
    Get a logger configured with the class name of the supplied C{instance}.

    @param instance: the instance; must not be C{None}.
    @return: a logger; never C{None}.
    """

    assert instance is not None, 'The instance is required.'

    _class = instance.__class__
    name = '.'.join((_class.__module__, _class.__name__))
    return logging.getLogger(name)


def default(value, the_default):
    return the_default() if value is None else value


class CallableMapperMixin(object):
    def __call__(self, *args, **kwargs):
        return self.map(*args, **kwargs)

    def map(self, *args, **kwargs):
        raise NotImplementedError('Abstract method.')

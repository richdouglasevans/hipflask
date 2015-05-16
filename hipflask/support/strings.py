# -*- coding: utf-8 -*-
"""
String-related utility methods.
"""

import re


MODULE_SEPARATOR = '.'


def is_stringy(thing):
    return isinstance(thing, basestring)


def collapse(xs):
    return [safe_string(x) for x in xs if (x is not None and len(safe_string(x)) > 0)]


def message_from(e):
    if hasattr(e, 'message'):
        return message_from(getattr(e, 'message'))
    else:
        message = e if is_stringy(e) else str(e)
    return safe_string(message)


def has_text(s):
    return s is not None and len(s.strip()) > 0


def safe_string(s, encoding='utf-8'):
    try:
        return ''.encode(encoding) if s is None else s.encode(encoding).strip()
    except LookupError:
        raise UnknownEncodingException.for_unknown_encoding(encoding)


def prefix_with(prefix, assets, separator='/'):
    """
    Prefix the supplied assets with the supplied prefix.
    """

    return map(lambda asset: "%s%s%s" % (prefix, separator, asset), assets)


camelcase_pattern = re.compile(r'([A-Z])')
underscore_pattern = re.compile(r'_([a-z])')


def camelcase_to_underscore(name):
    return camelcase_pattern.sub(lambda x: '_' + x.group(1).lower(), name)


def underscore_to_camelcase(name):
    return underscore_pattern.sub(lambda x: x.group(1).upper(), name)


def convert_keys(d, convert, skip_conversion=None):
    if skip_conversion is None:
        skip_conversion = lambda key: False

    def convert_keys_(av):
        if isinstance(av, dict):
            return convert_keys(av, convert, skip_conversion=skip_conversion)
        else:
            return av

    sink = {}
    for k, v in d.iteritems():
        the_key = k
        if not skip_conversion(k):
            the_key = convert(k)
        if isinstance(v, dict):
            sink[the_key] = convert_keys(v, convert, skip_conversion=skip_conversion)
        elif isinstance(v, (list, tuple)):
            sink[the_key] = map(convert_keys_, v)
        else:
            sink[the_key] = v
    return sink


class UnknownEncodingException(Exception):
    def __init__(self, message):
        self.message = message

    @staticmethod
    def for_unknown_encoding(name):
        """
        Thrown when an encoding cannot be looked up by name.

        @param name: the name of the unknown encoding.
        @return: an C{UnknownEncodingException}; never C{None}.
        """

        return UnknownEncodingException('Cannot find encoding with name "{}".'.format(name))

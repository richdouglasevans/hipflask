# -*- coding: utf-8 -*-
"""
Collections-related utility methods.
"""


def has_elements(l):
    return l is not None and len(l) > 0


def copy_and_update(source, **updates):
    assert source is not None, 'The source is required.'

    result = source.copy()
    if updates:
        result.update(updates)
    return result


def copy_and_append(source, updates):
    assert source is not None, 'The source is required.'

    result = list(source)
    if updates:
        result.append(updates)
    return result

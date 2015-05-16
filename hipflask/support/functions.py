# -*- coding: utf-8 -*-


def identity(o):
    """
    The identity function.

    @param o: the argument to be returned; can be L{None}.
    @return: C{o}, always.
    """

    return o


# noinspection PyUnusedLocal
def noop(*args, **kwargs):
    """
    The "no operation" function: it does nothing.
    """

    pass


# noinspection PyUnusedLocal
def is_truthy(value, *args, **kwargs):
    return bool(value)

# -*- coding: utf-8 -*-

from importlib import import_module
from pkgutil import iter_modules


def filter_module(package_name, package_path, predicate):
    for _, name, _ in iter_modules(package_path):
        module_name = '{}.{}'.format(package_name, name)
        module = import_module(module_name)
        for item in dir(module):
            item = getattr(module, item)
            if predicate(item):
                yield (item, module)


# -*- coding: utf-8 -*-
import inspect
import logging

from injector import Module
from hipflask.support.modules import filter_module


def discover_injection_modules(packages):
    for package in packages:
        name, path = package
        for item, module in filter_module(name, path, is_injection_module):
            _logger.debug('Found injection module [%s] in [%s].', item.__name__, module.__name__)
            yield item


def is_injection_module(item):
    return inspect.isclass(item) \
           and issubclass(item, Module) \
           and item.__name__ is not Module.__name__


_logger = logging.getLogger(__name__)

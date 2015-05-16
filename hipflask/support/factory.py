# -*- coding: utf-8 -*-
"""
L{flask.Flask} application customisation.
"""
import logging
from pkgutil import os

from flask import Flask, Blueprint
from flask.ext.injector import FlaskInjector
from flask_environments import Environments
from hipflask.support import default
from hipflask.support.collections import has_elements
from hipflask.support.injection import discover_injection_modules
from hipflask.support.modules import filter_module


def create_app(package_name, package_path, settings_override=None, settings='settings.yaml'):
    """
    Create a L{flask.Flask} application with common configuration applied.

    @param package_name: application package name.
    @param settings_override: a dictionary of settings to override.
    @return: the Flask application; never C{None}.
    """

    app = Flask(package_name, instance_relative_config=True)

    env = Environments(app)
    env.from_yaml(os.path.join(os.getcwd(), '', settings))
    app.config.from_object(settings_override)

    logging.basicConfig(level=logging.DEBUG)

    register_blueprints(app, package_name, package_path)
    register_injection_modules(app, package_name, package_path, settings_override=settings_override)

    return app


def register_blueprints(app, package_name, package_path):
    """
    Register all Blueprint instances on the supplied L{flask.Flask} application
    found in all modules for the specified package.

    @param app: the Flask application; must not be C{None}.
    @param package_name: the package name.
    @param package_path: the package path.
    """

    def is_blueprint(item):
        return isinstance(item, Blueprint)

    blueprints = list(filter_module(package_name, package_path, is_blueprint))
    _logger.debug('Registering [%d] blueprints on [%s].', len(blueprints), app)
    for blueprint, module in blueprints:
        _logger.debug('Registering blueprint from [%s] on [%s].', module.__name__, app)
        app.register_blueprint(blueprint)


def register_injection_modules(app, package_name, package_path, settings_override=None):
    """
    Register all Injector Modules on the supplied L{flask.Flask} application
    found in all modules for the specified package.

    @param app: the Flask application; must not be C{None}.
    @param package_name: the package name.
    @param package_path: the package path.
    """

    settings_override = default(settings_override, lambda: dict())

    def assemble_packages():
        packages = [(package_name, package_path)]
        extra_injection_modules = settings_override.get('injection_modules', [])
        packages.extend(extra_injection_modules)
        return packages

    injection_modules = list(discover_injection_modules(assemble_packages()))

    if has_elements(injection_modules):
        _logger.debug('Registering [%d] injection modules on [%s].', len(injection_modules), app)
    else:
        _logger.debug('Didn\'t find any injection modules to register on [%s].', app)

    injector = FlaskInjector(app=app, modules=injection_modules)
    # noinspection PyUnresolvedReferences
    app.extensions['Injector'] = injector.injector


_logger = logging.getLogger(__name__)

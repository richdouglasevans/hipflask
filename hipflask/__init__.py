# -*- coding: utf-8 -*-

from functools import wraps
import logging

import assets
from hipflask.support import factory
from hipflask.support.web import *
from hipflask.support.web.responsifiers import *
from hipflask.support.web.resolvers import SimpleSuffixBasedViewResolver


_logger = logging.getLogger(__name__)


def create_app(settings_override=None):
    app = factory.create_app(__name__, __path__, settings_override)
    initialise_web(app)
    assets.prepare(app)
    return app


def route(blueprint, *args, **kwargs):
    kwargs['strict_slashes'] = kwargs.get('strict_slashes', False)

    def decorator(f):
        @blueprint.route(*args, **kwargs)
        @wraps(f)
        def wrapper(*the_args, **the_kwargs):
            response_data = f(*the_args, **the_kwargs)
            return respond(response_data, *the_args, **the_kwargs)

        return wrapper

    return decorator


def initialise_web(app):
    html_responsifier = TemplatedResponsifier(SimpleSuffixBasedViewResolver())
    responsifiers = dict(html=html_responsifier, json=SimpleJsonResponsifier())
    app.responsifier = ContentNegotiatingResponsifier(responsifiers)

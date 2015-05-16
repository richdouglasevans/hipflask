# -*- coding: utf-8 -*-
from httplib import UNSUPPORTED_MEDIA_TYPE

from hipflask.support.collections import copy_and_update, has_elements
from werkzeug.datastructures import MIMEAccept
from werkzeug.http import parse_accept_header
from flask import request, render_template, jsonify, make_response
from werkzeug.exceptions import abort


class SimpleJsonResponsifier(object):
    """
    Create a C{Response} by rendering the model directly to JSON.
    """

    # noinspection PyUnusedLocal,PyMethodMayBeStatic
    def responsify(self, *args, **kwargs):
        view_model = args[0]
        return jsonify(**view_model)


class TemplatedResponsifier(object):
    """
    Create a C{Response} by rendering a (Jinja2) template.
    """

    def responsify(self, *args, **kwargs):
        view = self.view_resolver.resolve_view(*args, **kwargs)
        view_model = self.view_model(*args, **kwargs)
        content = render_template(view, **view_model)
        return make_response(content)

    # noinspection PyMethodMayBeStatic
    def view_model(self, *args, **kwargs):
        return copy_and_update(args[0], **kwargs)

    def __init__(self, view_resolver):
        super(TemplatedResponsifier, self).__init__()

        assert view_resolver, 'The view resolver is required.'
        self.view_resolver = view_resolver


class ContentNegotiatingResponsifier(object):
    def responsify(self, *args, **kwargs):
        content_type = self.best_content_type(request.headers['Accept'])
        responsifier = self.find_responsifier_for(content_type)

        if responsifier:
            return responsifier.responsify(*args, **kwargs)
        else:
            abort(UNSUPPORTED_MEDIA_TYPE)

    # noinspection PyMethodMayBeStatic
    def best_content_type(self, accept_header):
        accepts = parse_accept_header(accept_header, cls=MIMEAccept)
        return accepts.best

    JSON_CONTENT_TYPE = ('application/json', 'text/javascript')
    HTML_CONTENT_TYPE = ('text/html', 'application/xhtml+xml', 'application/xhtml+xml')

    def find_responsifier_for(self, best_type):
        responsifier = None
        if best_type in self.HTML_CONTENT_TYPE:
            responsifier = self.responsifiers['html']
        elif best_type in self.JSON_CONTENT_TYPE:
            responsifier = self.responsifiers['json']
        elif best_type == 'text/plain':
            responsifier = self.responsifiers['json']
        return responsifier

    def __init__(self, responsifiers):
        super(ContentNegotiatingResponsifier, self).__init__()

        assert has_elements(responsifiers), 'The responsifiers are required.'
        self.responsifiers = dict(responsifiers)

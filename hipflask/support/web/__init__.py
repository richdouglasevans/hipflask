# -*- coding: utf-8 -*-
"""
Web- and Flask-related extensions.
"""

from httplib import OK

from hipflask.support import CodedError, HipflaskException
from hipflask.support.strings import is_stringy, has_text
from werkzeug.wrappers import Response
from flask import request, current_app

HEADER_LOCATION = 'Location'
HEADER_CONTENT_TYPE = 'Content-Type'

METHOD_GET = 'GET'
METHOD_PUT = 'PUT'
METHOD_POST = 'POST'
METHOD_PATCH = 'PATCH'
METHOD_DELETE = 'DELETE'
METHOD_OPTIONS = 'OPTIONS'

CONTENT_TYPE_APPLICATION_JSON = 'application/json'

ERROR_BAD_REPRESENTATION = CodedError(100, message='The representation is bad.')


# noinspection PyUnusedLocal
def get_request_json(*args, **kwargs):
    return request.get_json(silent=True)


def current_environment(app=current_app):
    """
    Look up the current environment; forex, C{DEVELOPMENT} or C{TESTING}.

    This function exists just to keep an unfortunate typo in one place:
    U{github.com/mattupstate/flask-environments/pull/2#issuecomment-30771313}

    @param app: the app to be interrogated; must not be C{None}.
    @return: the current environment; never C{None}.
    """

    return app.config.get('ENVIORNMENT', 'DEVELOPMENT')  # typo intentional


def set_response_header(response, key, value):
    """
    Set the C{key} header of the C{response} to the supplied C{value}.

    @param response: the C{Response}.
    @param key: the header name.
    @param value: the header value.
    @return: the C{response}, for chaining.
    """

    response.headers[key] = value
    return response


def set_header_location(response, location):
    """
    Set the C{Location} header of the C{response} to the supplied C{location}.

    @param response: the C{Response}.
    @param location: the location.
    @return: the C{response}, for chaining.
    """

    return set_response_header(response, HEADER_LOCATION, location)


def set_header_content_type(response, content_type):
    """
    Set the C{Content-Type} header of the C{response} to the supplied C{content_type}.

    @param response: the C{Response}.
    @param content_type: the content-type.
    @return: the C{response}, for chaining.
    """

    return set_response_header(response, HEADER_CONTENT_TYPE, content_type)


def respond(response_data, *args, **kwargs):
    """
    Create a C{Response}.

    @param response_data: metadata about the response such as the view to be rendered.
    @param args: other positional arguments.
    @param kwargs: other named arguments.
    @return: a C{Response}; never C{None}.
    """

    if isinstance(response_data, Response):
        response = response_data
    else:
        (view_name, model, status_code) = deconstruct(response_data)
        responsifier = current_app.responsifier
        response = responsifier.responsify(model,
                                           status_code=status_code,
                                           view_name=view_name,
                                           *args, **kwargs)
        response.status_code = status_code
    return response


def deconstruct(response_data):
    """
    Deconstruct the supplied C{response_data} into its constituent web-related elements.

    Returns a tuple of the form:

        C{(<view_name(string)>, <model(dict)>, <(HTTP) status_code(int)>)}

    @param response_data: that which is returned by a Controller; must not be C{None}.
    @return: the constituent web-related elements as a tuple; never C{None}.
    """

    assert response_data is not None, 'The response data is required.'

    if is_stringy(response_data):
        return deconstruct_string(response_data)
    elif isinstance(response_data, (tuple, list)):
        return deconstruct_list(response_data)
    elif isinstance(response_data, dict):
        return deconstruct_dict(response_data)


def deconstruct_string(response_data):
    view_name = required_view_name(response_data)
    return view_name, {}, OK


def deconstruct_list(response_data, model=None, status_code=OK):
    view_name = None
    if not response_data:
        raise HipflaskException('Response data is empty; the view name at least is required.')
    if len(response_data) >= 1:
        view_name = required_view_name(response_data[0])
    if len(response_data) >= 2:
        model = response_data[1]
    if len(response_data) >= 3:
        status_code = response_data[2]

    if model is None:
        model = {}
    if status_code is None:
        status_code = OK

    return view_name, model, status_code


def deconstruct_dict(response_data):
    view_name = required_view_name(response_data.get('view_name', None))
    model = response_data.get('model', {})
    status_code = response_data.get('status_code', OK)

    if model is None:
        model = response_data

    return view_name, model, status_code


def required_view_name(view_name):
    if not is_stringy(view_name):
        raise HipflaskException('Required view name must be a string.')
    if not has_text(view_name):
        raise HipflaskException('Required view name is empty.')
    return view_name

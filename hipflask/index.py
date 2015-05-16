# -*- coding: utf-8 -*-

import logging

from flask import Blueprint
from hipflask import route

_logger = logging.getLogger(__name__)

index = Blueprint('index', __name__)


@route(index, '/')
def display_homepage():
    return 'index', {}

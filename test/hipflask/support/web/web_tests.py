# -*- coding: utf-8 -*-

import unittest

from hamcrest import *
from hipflask.support.web import *


AN_ABSOLUTE_URL = 'http://www.google.com/'


# noinspection PyClassHasNoInit
class StubResponse():
    headers = {}


class SetHeaderLocationTests(unittest.TestCase):
    response = None

    def setUp(self):
        self.response = StubResponse

    def test_sunny_day(self):
        expected_location = AN_ABSOLUTE_URL
        set_header_location(self.response, expected_location)
        assert_that(self.response.headers, has_key('Location'),
                    'The "Location" must be added to the headers.')
        location = self.response.headers[HEADER_LOCATION]
        assert_that(location, is_(expected_location))


class SetHeaderContentTypeTests(unittest.TestCase):
    response = None

    def setUp(self):
        self.response = StubResponse

    def test_sunny_day(self):
        expected_content_type = CONTENT_TYPE_APPLICATION_JSON
        set_header_content_type(self.response, expected_content_type)
        assert_that(self.response.headers, has_key(HEADER_CONTENT_TYPE),
                    'The "Content-Type" must be added to the headers.')
        content_type = self.response.headers[HEADER_CONTENT_TYPE]
        assert_that(content_type, is_(expected_content_type))

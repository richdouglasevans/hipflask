# -*- coding: utf-8 -*-

import unittest

# noinspection PyPackageRequirements
from bson.objectid import ObjectId
# noinspection PyPackageRequirements
from bson.errors import InvalidId
from hipflask.support.mongo import ToObjectIdMapper, ObjectIdToStringMapper

OBJECT_ID_STRING_VALID = '52b06645a337b7276fee4a8f'
OBJECT_ID_STRING_INVALID = 'an invalid ObjectId'


class ToObjectIdMapperTests(unittest.TestCase):
    def setUp(self):
        super(ToObjectIdMapperTests, self).setUp()
        self.mapper = ToObjectIdMapper()

    def test_map_with_none(self):
        self.assertRaises(TypeError, self.mapper.map, None)

    def test_map_with_unsupported_object(self):
        self.assertRaises(TypeError, self.mapper.map, [])

    def test_map_with_invalid_ObjectId(self):
        self.assertRaises(InvalidId, self.mapper.map, OBJECT_ID_STRING_INVALID)

    def test_map_with_string(self):
        oid = self.mapper.map(OBJECT_ID_STRING_VALID)
        self.assertIsNotNone(oid)

    def test_map_with_string_unicode(self):
        oid = self.mapper.map(unicode(OBJECT_ID_STRING_VALID))
        self.assertIsNotNone(oid)

    def test_map_with_ObjectId(self):
        oid = self.mapper.map(ObjectId(OBJECT_ID_STRING_VALID))
        self.assertIsNotNone(oid)


class ObjectIdToStringMapperTests(unittest.TestCase):
    def setUp(self):
        super(ObjectIdToStringMapperTests, self).setUp()
        self.mapper = ObjectIdToStringMapper()

    def test_map_with_none(self):
        oid = self.mapper.map(None)
        self.assertIsNone(oid)

    def test_map_with_string(self):
        oid_astr = OBJECT_ID_STRING_VALID
        oid = self.mapper.map(oid_astr)
        self.assertEqual(oid_astr, oid)

    def test_map_with_ObjectId(self):
        oid_astr = OBJECT_ID_STRING_VALID
        oid = self.mapper.map(ObjectId(oid_astr))
        self.assertEqual(oid_astr, oid)

    def test_map_with_unsupported_object(self):
        self.assertRaises(TypeError, self.mapper.map, [])

    def test_map_with_invalid_ObjectId(self):
        self.assertRaises(TypeError, self.mapper.map, OBJECT_ID_STRING_INVALID)

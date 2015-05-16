# -*- coding: utf-8 -*-

# noinspection PyPackageRequirements
import datetime

from bson.objectid import ObjectId
from hipflask.support import logger_for, CallableMapperMixin
import simplejson as json
from hipflask import CodedError, is_stringy

ERROR_ID_INVALID = CodedError(1, message='The ID is invalid.')


class MongoJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        elif isinstance(obj, ObjectId):
            return unicode(obj)
        return json.JSONEncoder.default(self, obj)


class ToObjectIdMapper(CallableMapperMixin):
    def map(self, o):
        if o is None:
            raise TypeError('Cannot map from None to ObjectId.')
        elif is_stringy(o):
            oid = ObjectId(o)
        elif isinstance(o, ObjectId):
            oid = o
        else:
            raise TypeError('Cannot map from [{}] to ObjectId.'.format(o))
        return oid


class ObjectIdToStringMapper(CallableMapperMixin):
    def map(self, o):
        if o is None:
            oid = None
        elif isinstance(o, ObjectId):
            oid = unicode(o)
        elif is_stringy(o):
            if ObjectId.is_valid(o):
                oid = unicode(o)
            else:
                raise TypeError('Invalid object ID [{}].'.format(o))
        else:
            raise TypeError('Cannot map from [{}] to string.'.format(o))
        return oid


class MongoRepositoryMixin(object):
    def __init__(self, db):
        assert db is not None, 'The Mongo DB is required.'

        self._db = db

        self._logger = logger_for(self)

    def __getattr__(self, item):
        # attribute name is interpreted as collection name
        return self._db[item]

    @property
    def db(self):
        return self._db

    def __str__(self):
        return '{} {}'.format(self.__class__.__name__, self._db)


class IdBased(object):
    """
    A mixin for classes that support an ID value.
    """

    # noinspection PyShadowingBuiltins,PyUnusedLocal
    def __init__(self, id=None, *args, **kwargs):
        self._id = id

    @property
    def id(self):
        """
        Return the persistent identity value.

        Will be L{None} if this instance is transient.
        """

        return self._id

    def is_persistent(self):
        """
        Is this instance persistent?

        An ID value that is not L{None} indicates persistence.

        @return: C{True} iff this class is persistent.
        """

        return self._id is not None

    def is_transient(self):
        """
        Is this instance transient?

        An ID value that is L{None} indicates transience.

        @return: C{True} iff this class is transient.
        """

        return not self.is_persistent()


def munge_id(document, id_mapper):
    """
    "Munge" the C{id} of the supplied document.

    Removes any C{id} and replaces it with an C{_id} that is an C{ObjectID}
    (or whatever the supplied C{id_mapper} maps the C{id} to. This ensures
    a consistent interface at the MongoDB-level: the ID is always a field
    called C{_id} which follows the naming pattern of MongoDB itself.

    If the supplied C{id_mapper} is C{None}, a C{ToObjectIdMapper} is used.

    @param document: the document to be munged; must not be C{None}.
    @param id_mapper: maps any C{id} to an C{ObjectID}; can be C{None}.
    """

    if id_mapper is None:
        id_mapper = ToObjectIdMapper()

    _id = document.pop('id', None)
    if _id is not None:
        document['_id'] = id_mapper(_id)

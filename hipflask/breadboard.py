# -*- coding: utf-8 -*-

import logging

from flask import Config
from injector import Module, singleton, inject, provides
from pymongo import MongoClient
from pymongo.database import Database


class MongoModule(Module):
    @inject(config=Config)
    @provides(MongoClient, scope=singleton)
    def provide_mongo_client(self, config):
        url = get_required_value(config, 'MONGO_URL')
        connect_eagerly = config.get('MONGO_CONNECT_EAGERLY', True)

        _logger.debug('Mongo connection [url=%s].', url)

        return MongoClient(url, connect_eagerly)

    @inject(config=Config, mongo_client=MongoClient)
    @provides(Database, scope=singleton)
    def provide_mongo_db(self, config, mongo_client):
        db_name = get_required_value(config, 'MONGO_DB')

        _logger.debug('Mongo database [name=%s].', db_name)

        return mongo_client[db_name]


def get_required_value(config, key):
    value = config.get(key, None)
    if value is None:
        raise Exception('No value for [%s]; check your configuration.', key)
    return value


_logger = logging.getLogger(__name__)

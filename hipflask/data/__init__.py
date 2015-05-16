# -*- coding: utf-8 -*-

import logging

from flask import Config
from injector import inject, singleton, Module, provides
from pymongo import MongoClient
from hipflask.support import DEVELOPMENT, default
from yaml import load_all


class DataSetMixin(object):
    def __init__(self, environment=DEVELOPMENT):
        super(DataSetMixin, self).__init__()

        self.environment = default_to_development(environment)

    def _load(self, data_file):
        datafile = self._data_file(data_file)
        with open(datafile, 'r') as stream:
            data = load_all(stream)
            for datum in data:
                yield datum

    def _data_file(self, name):
        package = __package__.replace('.', '/')
        return '{}/{}/{}.yaml'.format(package, self.environment, name)


class GoldenDataSet(DataSetMixin):
    def __init__(self, database_dropper=None, example_data_set=None, environment=DEVELOPMENT):
        super(GoldenDataSet, self).__init__(environment=environment)

        self.database_dropper = database_dropper
        self.example_data_set = example_data_set

    def load(self):
        self.database_dropper.drop()

        _logger.info('Loading data into the [%s] environment.', self.environment)
        list(self.example_data_set.load())


class ExampleDataSet(DataSetMixin):
    def load(self):
        for example in self._load('example'):
            _logger.info('Loading [%s].', example)


class DatabaseDropper(object):
    @inject()
    def __init__(self, mongo_client=None, db_name=None):
        super(DatabaseDropper, self).__init__()

        self.db_name = db_name
        self.mongo_client = mongo_client

    def drop(self):
        _logger.info('Dropping [%s] database prior to data loading.', self.db_name)

        self.mongo_client.drop_database(self.db_name)


class GoldenDataSetModule(Module):
    @inject(example_data_set=ExampleDataSet, database_dropper=DatabaseDropper)
    @provides(GoldenDataSet, scope=singleton)
    def provide_golden_data_set(self, example_data_set, database_dropper):
        return GoldenDataSet(example_data_set=example_data_set, database_dropper=database_dropper)

    @provides(ExampleDataSet, scope=singleton)
    def provide_example_data_set(self):
        return ExampleDataSet()

    @inject(config=Config, mongo_client=MongoClient)
    @provides(DatabaseDropper, scope=singleton)
    def provide_database_dropper(self, mongo_client, config):
        db_name = config.get('MONGO_DB', None)
        if db_name is None:
            raise Exception('No value for [%s]; check your configuration.', 'MONGO_DB')

        return DatabaseDropper(mongo_client=mongo_client, db_name=db_name)


def default_to_development(environment):
    return (default(environment, lambda: DEVELOPMENT)).lower()


_logger = logging.getLogger(__name__)

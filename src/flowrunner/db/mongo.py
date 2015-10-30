#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs
from pluck import pluck

from pymongo import MongoClient
from flowrunner.utils import rget, rpluck
from flowrunner.utils.json_preprocessor import JsonPreprocessor
from flowrunner.utils.logger import Logger
from flowrunner.utils.strings import read_json

logger = Logger(__name__)


class Collections(object):
    def __init__(self, db):
        """
        :type db: pymongo.database.Database
        """
        self._collections = set(db.collection_names())
        self.environment = db.get_collection('environment')
        self.calibration = db.get_collection('calibration')

    def exists(self, collection):
        return collection in self._collections

    def __repr__(self):
        mandatory = ['environment', 'calibration']
        return "<Collections: {status}>".format(status=', '.join(
            ["{name}={status}".format(name=name, status=name in self._collections)
             for name in set(mandatory).union(self._collections)]))


class MongoDB(object):
    def __init__(self, host='localhost', port=27017, database='flow'):
        self.client = MongoClient(host, port)
        self.flowdb = self.client.get_database(database)
        self.collections = Collections(self.flowdb)

        if not self.collections.exists('environment'):
            self._create_collection_environment()

        if not self.collections.exists('calibration'):
            self._create_collection_calibration()

    def _create_collection_environment(self, name='environment'):
        logger.debug("creating collection '{name}'...".format(name=name))
        self.flowdb.create_collection(name)

        with logger:
            logger.debug("creating indices for collection '{name}'".format(name=name))
            self._create_indices(self.collections.environment, [
                # cpu indices
                'arch.cpu.x64',
                'arch.cpu.frequency',
                'arch.cpu.avail',
                # memory indices
                'arch.memory.avail'
            ])

    def _create_collection_calibration(self, name='calibration'):
        logger.debug("creating collection '{name}'...".format(name=name))
        self.flowdb.create_collection(name)

        with logger:
            logger.debug("creating indices for collection '{name}'".format(name=name))
            self._create_indices(self.collections.environment, [
                'cpu', 'memory',
            ])

    @staticmethod
    def _create_indices(collection, indices):
        """
        :type collection:  pymongo.collection.Collection
        :type indices: list
        """
        with logger:
            for index in indices:
                logger.debug("creating index '{index}'".format(index=index))
                collection.create_index(index)

    def insert_environment(self, filename):
        """
        Method will process given json filename and will insert it into
            database, collection environment. Method will also remove entries
            having no information (like missing binaries)
        :rtype : pymongo.results.InsertOneResult
        :type filename: str
        """
        json_data = read_json(filename)
        JsonPreprocessor.filter(json_data['bins'], 'missing', lambda x: bool(x))
        return self.collections.environment.insert_one(json_data)

    def insert_calibration(self, filename):
        """
        Method will process given json filename and will insert it into
            database, collection calibration. Processing json is done by analyzing measured
            values in json file. Only 3 values (cpu, memory, combination) will be stored in db
        :rtype : pymongo.results.InsertOneResult
        :type filename: str
        """
        json_data = read_json(filename)
        calibration = {
            'cpu': sum(rpluck(json_data, 'tests.for-loop.effectiveness')),
            'memory': sum(rpluck(json_data, 'tests.string-concat.effectiveness')),
            'complex': sum(rpluck(json_data, 'tests.matrix-solve.effectiveness'))
        }
        return self.collections.calibration.insert_one(calibration)

    def remove_all(self):
        return self.client.drop_database('flow')


m = MongoDB()
m.remove_all()
# print m.insert_environment(r'c:\Users\Jan\Dropbox\meta\test-04\environment.json')
# print m.insert_calibration(r'c:\Users\Jan\Dropbox\meta\test-04\performance.json')

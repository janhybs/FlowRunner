#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs
from datetime import datetime

from pymongo import MongoClient
from flowrunner.utils import rget, rpluck
from flowrunner.utils.json_preprocessor import JsonPreprocessor
from flowrunner.utils.logger import Logger
from flowrunner.utils.strings import read_json, to_json, secure_values
from flowrunner.utils import io, lists

logger = Logger(__name__)


class Collections(object):
    def __init__(self, db):
        """
        :type db: pymongo.database.Database
        """
        self._collections = set(db.collection_names())
        self.environment = db.get_collection('environment')
        self.calibration = db.get_collection('calibration')
        self.context = db.get_collection('context')
        self.pts = db.get_collection('pts')

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

        if not self.collections.exists('context'):
            self._create_collection_context()

        if not self.collections.exists('pts'):
            self._create_collection_pts()

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

    def _create_collection_context(self, name='context'):
        logger.debug("creating collection '{name}'...".format(name=name))
        self.flowdb.create_collection(name)

        with logger:
            logger.debug("creating indices for collection '{name}'".format(name=name))
            self._create_indices(self.collections.environment, [
                'nproc', 'task_size', 'problem'
            ])

    def _create_collection_pts(self, name='pts'):
        logger.debug("creating collection '{name}'...".format(name=name))
        self.flowdb.create_collection(name)

        with logger:
            logger.debug("creating indices for collection '{name}'".format(name=name))
            self._create_indices(self.collections.environment, [
                'path', 'children', 'parent'
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

    @staticmethod
    def _extract_context(json_data):
        fields = dict(flags='program-flags', branch='program-branch', problem='problem',
                      path='path', task_size='task-size', resolution='timer-resolution',
                      start='run-started-at', nproc='nproc')

        context = JsonPreprocessor.extract_props(json_data, fields)
        context = JsonPreprocessor.convert_fields(context, lambda x: datetime.strptime(x, '%m/%d/%y %H:%M:%S'),
                                                  ['start'])
        return context

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

    def insert_context(self, context):
        return self.collections.context.insert_one(context)

    def insert_process(self, dirname):
        profilers = io.browse(dirname)
        profilers = lists.filter(profilers, lambda x: str(x).lower().endswith("8.json"))

        for profiler in profilers:
            json_data = read_json(profiler)
            context = self._extract_context(json_data)
            context_id = self.insert_context(context).inserted_id

            whole_program = json_data['children'][0]

            self.insert_time_frame(whole_program, [], ctxt_id=context_id)

    def insert_time_frame(self, node, path, **kwargs):
        """
        :type node: dict
        :type path: list
        """
        new_path = path[:]
        new_path.append(node.get('tag'))
        print to_path(secure_values(new_path))

        for child in node.get('children', []):
            self.insert_time_frame(child, new_path, **kwargs)


def to_path(values):
    return '/' + '/'.join(values)


m = MongoDB()
# m.remove_all()
# print m.insert_environment(r'c:\Users\Jan\Dropbox\meta\test-04\environment.json')
# print m.insert_calibration(r'c:\Users\Jan\Dropbox\meta\test-04\performance.json')
m.collections.context.remove({})
print m.insert_process(r'c:\Users\Jan\Dropbox\meta\test-04\01_Melechov_56355')

#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs

from flowrunner.db.mongo import MongoDB
from flowrunner.utils import io, lists
from flowrunner.utils.logger import Logger
from flowrunner.utils.timer import Timer


logger = Logger(__name__)
timer = Timer()


class Experiments(object):
    def __init__(self, mongo):
        """
        :type mongo: flowrunner.db.mongo.MongoDB
        """
        self.mongo = mongo

    def insert_one(self, dirname):
        with timer.measured('Processing one, folder {dirname}'.format(dirname=dirname), False):
            env = self.mongo._extract_environment(io.join_path(dirname, 'environment.json'))
            cal = self.mongo._extract_calibration(io.join_path(dirname, 'performance.json'))

            env['cal'] = cal

            self.mongo.insert_process(dirname, env)

    def insert_many(self, dirname, filters=[]):
        dirs = io.listdir(dirname)
        dirs = lists.filter(dirs, lambda x: io.name_starts_with(x, 'test'))

        with timer.measured('Processing many, folder {dirname}'.format(dirname=dirname), False):
            for dir in dirs:
                self.insert_one(dir)

mongo = MongoDB()
mongo.remove_all()
mongo.close()
mongo = MongoDB()

experiments = Experiments(MongoDB())
experiments.insert_many('/home/jan-hybs/Dropbox/meta', [lambda x: str(x).startswith('test')])
# experiments.insert_one('/home/jan-hybs/Dropbox/meta/test-13')
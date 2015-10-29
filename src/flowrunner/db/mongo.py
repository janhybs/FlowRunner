#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs


from pymongo import MongoClient


class MongoDB(object):
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.flowdb = self.client.get_database('flow')
        self.collections = set(self.flowdb.collection_names())

        self.arch = self.create_collection('arch')
        self.metrics = self.create_collection('metrics')
        self.context = self.create_collection('context')

        self.create_indices()

    def create_collection(self, name):
        if name in self.collections:
            return self.flowdb[name]

        print 'Creating collection {name}'.format(name=name)
        return self.flowdb.create_collection(name)

    def connect(self):
        self.client = MongoClient('localhost', 27017)

    def create_indices(self):
        print self.arch.create_index("arch.cpu")
        print self.arch.create_index("arch.memory")
        print self.arch.create_index("arch.system")

    def remove_all(self):
        return self.client.drop_database('flow')


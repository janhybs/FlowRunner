#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs

from multiprocessing import Process, Event, Value


class AbstractProcess(Process):
    def __init__(self, ):
        Process.__init__(self)
        self.exit = Event()
        self.result = Value('f', 0)
        self.terminated = None

    def run(self):
        self.test(self.result)

    def shutdown(self):
        if self.is_alive():
            self.exit.set()
            self.terminated = True
        else:
            self.terminated = False

    def test(self, result):
        pass
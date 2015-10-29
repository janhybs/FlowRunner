#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs

from time import time

from flowrunner.runner.execution.plugins.absplugin import AbstractExecutorPlugin


class PluginTimer(AbstractExecutorPlugin):
    def __init__(self):
        self.time_start = None
        self.time_end = None
        self.duration = None

    def start(self, process, plugins):
        super(PluginTimer, self).start(process, plugins)
        self.time_start = time()

    def end(self, exit_code):
        super(PluginTimer, self).end(exit_code)
        self.time_end = time()
        self.duration = self.time_end - self.time_start

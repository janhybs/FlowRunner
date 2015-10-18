#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs

from runner.execution.plugins.absplugin import AbstractExecutorPlugin


class PluginEnv(AbstractExecutorPlugin):
    def __init__(self, env={ }):
        self.env = env
#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs

from __future__ import print_function
import re
from colorama import init
from termcolor import colored
from runner.execution.plugins.absplugin import AbstractExecutorPlugin

init()


class PluginBriefInfo(AbstractExecutorPlugin):
    def __init__(self, name, left_padding=' '*4):
        self.stdout_all = []
        self.stderr_all = []
        self.name = name
        self.left_padding = left_padding

    def end(self, exit_code):
        super(PluginBriefInfo, self).end(exit_code)
        print (
            colored(
                "{self.left_padding}task '{self.name:50s}' exited with code {self.process.exit_code}".format(self=self),
                color='white',
                on_color='on_green' if exit_code == 0 else 'on_red',
                attrs=['bold']
            )
        )


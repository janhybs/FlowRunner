# encoding: utf-8
# author:   Jan Hybs

from __future__ import print_function
import re
from colorama import init

from termcolor import colored

from flowrunner.runner.execution.plugins.absplugin import AbstractExecutorPlugin


init()


class PluginProgress(AbstractExecutorPlugin):
    CMAKE_PATTERN = r'\[\s*([0-9]+)%\]'

    def __init__(self, debug=True, pattern=CMAKE_PATTERN, source='stdout', name="Exec"):
        self.debug = debug
        self.regex = re.compile(pattern, re.MULTILINE)
        self.source = source
        self.progress = 0
        self.name = name

    def start(self, process, plugins):
        super(PluginProgress, self).start(process, plugins)
        self.progress = 0
        if self.debug:
            print(colored("command start '{:s}'".format(self.name), color='white', on_color='on_blue', attrs=['bold']))

    def end(self, exit_code):
        super(PluginProgress, self).end(exit_code)
        self.progress = 100
        if self.debug:
            print(colored("command end   '{:s}'".format(self.name), color='white', on_color='on_red' if exit_code != 0 else 'on_green', attrs=['bold']))

    def output(self, stdout, stderr):
        super(PluginProgress, self).output(stdout, stderr)

        lines = stdout if self.source == 'stdout' else stderr

        if lines:
            heystack = ' '.join(lines)
            match = self.regex.findall(heystack)
            if match:
                new_progress = match[-1]
                if self.progress != new_progress:
                    self.progress = new_progress
                    if self.debug:
                        print(colored('progress {:s}'.format(new_progress), color='white', on_color='on_green',
                                      attrs=['bold']))
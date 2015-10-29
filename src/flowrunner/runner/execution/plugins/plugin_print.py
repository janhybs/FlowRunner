# encoding: utf-8
# author:   Jan Hybs
from flowrunner.runner.execution.plugins.absplugin import AbstractExecutorPlugin


class PluginPrint(AbstractExecutorPlugin):
    def __init__(self, debug=True):
        self.stdout_all = []
        self.stderr_all = []
        self.debug = debug

    def output(self, stdout, stderr):
        super(PluginPrint, self).output(stdout, stderr)
        self.stdout_all.extend(stdout)
        self.stderr_all.extend(stderr)

    def end(self, exit_code):
        if self.stdout_all:
            if self.debug:
                print 'stdout: '
            print '\n'.join(self.stdout_all)

        if self.stderr_all:
            if self.debug:
                print 'stderr: '
            print '\n'.join(self.stderr_all)
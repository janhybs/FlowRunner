# encoding: utf-8
# author:   Jan Hybs
import os

from runner.execution.plugins.absplugin import AbstractExecutorPlugin


class PluginWrite(AbstractExecutorPlugin):
    def __init__(self, debug=False, stdout=None, stderr=None, purge=False):
        self.debug = debug
        self.stdout_file = stdout
        self.stderr_file = stderr

        if purge:
            try:
                os.remove(self.stdout_file)
                os.remove(self.stderr_file)
            except:
                if self.debug:
                    print ('no such file')

    def output(self, stdout, stderr):
        super(PluginWrite, self).output(stdout, stderr)

        if stdout and self.stdout_file:
            with open(self.stdout_file, 'a+') as fp:
                fp.write('\n'.join(stdout))
                fp.write('\n')

        if stderr and self.stderr_file:
            with open(self.stderr_file, 'a+') as fp:
                fp.write('\n'.join(stderr))
                fp.write('\n')
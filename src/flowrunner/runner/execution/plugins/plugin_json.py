# encoding: utf-8
# author:   Jan Hybs
import os

from flowrunner.runner.execution.plugins.absplugin import AbstractExecutorPlugin


class PluginJson(AbstractExecutorPlugin):
    def __init__(self, debug=False, stdout=None, stderr=None, purge=False, details={}):
        self.debug = debug
        self.stdout_file = stdout
        self.stderr_file = stderr
        self.stdout_all = []
        self.stderr_all = []
        self.details = details
        self.json = {}

        if purge:
            try:
                os.remove(self.stdout_file)
                os.remove(self.stderr_file)
            except:
                if self.debug:
                    print ('no such file')

    def output(self, stdout, stderr):
        super(PluginJson, self).output(stdout, stderr)
        if stdout:
            self.stdout_all.extend(stdout)
        if stderr:
            self.stderr_all.extend(stderr)

    def end(self, exit_code):
        super(PluginJson, self).end(exit_code)

        self.json['command'] = self.process.command
        self.json['exit_code'] = exit_code
        self.json['stdout'] = self.stdout_all
        self.json['stderr'] = self.stderr_all
        self.json.update(self.details)
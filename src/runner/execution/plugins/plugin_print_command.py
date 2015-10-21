# encoding: utf-8
# author:   Jan Hybs
from runner.execution.plugins.absplugin import AbstractExecutorPlugin


class PluginPrintCommand(AbstractExecutorPlugin):
    def __init__(self, debug=True):
        self.stdout_all = []
        self.stderr_all = []
        self.debug = debug

    def start(self, process, plugins):
        super(PluginPrintCommand, self).start(process, plugins)
        print 'command: {process.command}'.format(process=process)
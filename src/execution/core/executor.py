# encoding: utf-8
# author:   Jan Hybs
from execution.core.async import AsyncProcess
from execution.plugins.absplugin import Plugins


class Executor(object):
    def __init__(self, command, plugins=[]):
        self.command = command
        self.plugins = Plugins(plugins)
        self.process = None

    def run(self):
        self.process = AsyncProcess(self.command)
        self.plugins.process_start(self.process, self.plugins)
        (o, e) = self.process.run()

        while self.process.is_running():
            # get all stdout lines and emit them
            stdout = []
            while not o.empty():
                stdout.append(o.get())

            # get all stderr lines and emit them
            stderr = []
            while not e.empty():
                stderr.append(e.get())

            self.plugins.process_output(stdout, stderr)
            self.plugins.process_do_work()

        exit_code = self.process.wait()
        self.plugins.process_end(exit_code)
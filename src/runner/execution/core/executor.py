# encoding: utf-8
# author:   Jan Hybs
from runner.execution.core.async import AsyncProcess
from runner.execution.plugins.absplugin import Plugins


class Executor(object):
    def __init__(self, command, plugins=[]):
        self.command = command
        self.plugins = Plugins(plugins)
        self.process = None
        self.exit_code = None
        self.stdout = None
        self.stderr = None

    def run(self):
        self.stdout = []
        self.stderr = []
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

            self.stdout.extend(stdout)
            self.stderr.extend(stderr)
            self.plugins.process_output(stdout, stderr)
            self.plugins.process_do_work()

        self.exit_code = self.process.wait()
        self.plugins.process_end(self.exit_code)
        return self

    def __repr__(self):
        return "<Executor: '{self.command}'>".format(self=self)
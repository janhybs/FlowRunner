# encoding: utf-8
# author:   Jan Hybs


class Plugins(object):
    def __init__(self, plugins_lst=[]):
        self.plugins = dict()
        for plugin in plugins_lst:
            self.register(plugin)

    def get(self, plugin):
        return self.plugins.get(plugin, None)

    def register(self, plugin_instance):
        self.plugins[str(plugin_instance.__class__.__name__)] = plugin_instance

    def process_start(self, process, plugins):
        for plugin in self.plugins.values():
            plugin.start(process, plugins)

    def process_output(self, stdout, stderr):
        for plugin in self.plugins.values():
            plugin.output(stdout, stderr)

    def process_do_work(self, *args, **kwargs):
        for plugin in self.plugins.values():
            plugin.do_work(*args, **kwargs)

    def process_end(self, exit_code):
        for plugin in self.plugins.values():
            plugin.end(exit_code)


class AbstractExecutorPlugin(object):
    def __init__(self):
        self.plugins = None
        self.process = None

    def start(self, process, plugins):
        self.process = process
        self.plugins = plugins

    def output(self, stdout, stderr):
        pass

    def do_work(self, *args, **kwargs):
        pass

    def end(self, exit_code):
        pass

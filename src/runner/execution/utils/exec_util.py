#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs
from itertools import product

from runner.execution.core.executor import Executor
from utils.pluck_dict import PluckDict


def expand_vars(variables):
    expanded_vars = dict()
    for var in variables:
        name, value = var.split(':', 1)
        if name not in expanded_vars:
            expanded_vars[name] = []

        if value.find(' ') == -1 and value.find(':') == -1:
            expanded_vars[name].append(value)
        elif value.find(' ') != -1:
            expanded_vars[name].extend(value.split(' '))
        elif value.find(':') != -1:
            values = value.split(':')
            if len(values) == 2:
                step = 1
                start, stop = values
            elif len(values) == 3:
                start, step, stop = values
            else:
                raise Exception('unsupported number of elements in range')

            expanded_vars[name].extend(range(int(start), int(stop), int(step)))
    return expanded_vars


def expand_command(command, variables, plugin_generator):
    commands = list()
    plugins = list()
    for value in product(*variables.values()):
        env = dict(zip(variables.keys(), value))
        commands.append(command.format(**env))
        plugins.append(plugin_generator if not callable(plugin_generator) else plugin_generator(command, env))
    return commands, plugins


def exec_all(command, variables={}, plugin_generator=[]):
    commands, plugins = expand_command(
        command,
        expand_vars(variables) if type(variables) is list else variables,
        plugin_generator)

    result = []
    for i in range(len(commands)):
        ex = Executor(commands[i], plugins[i])
        result .append(ex.run())
    return PluckDict(result)
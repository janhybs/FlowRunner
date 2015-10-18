#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs

from itertools import product
from subprocess import check_output, PIPE, CalledProcessError, call
from runner.execution.core.executor import Executor
from runner.execution.plugins.plugin_env import PluginEnv


def check_exit_secure(command, **kwargs):
    return call(command, stderr=PIPE, shell=True, **kwargs)


def check_output_secure(command, **kwargs):

    try:
        return check_output(command, stderr=PIPE, shell=True, **kwargs)
    except CalledProcessError as e:
        return ''


def expand_vars(variables):
    """
    Method returns expanded variables. Variables are in format NAME=VALUE
        where value can be either string value, space separated values
        or range specification such as foo=0:10:2 (start:stop:step)
    :param variables:
    :return:
    """
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
                start, stop, step = values
            else:
                raise Exception('unsupported number of elements in range')

            expanded_vars[name].extend(range(int(start), int(stop), int(step)))
    return expanded_vars


def expand_command(command, variables, plugin_generator):
    """
    Method return tuple of commands, and plugins for each combination of given variables
    :param command:
    :param variables:
    :param plugin_generator:
    :return:
    """
    commands = list()
    plugins = list()
    for value in product(*variables.values()):
        env = dict(zip(variables.keys(), value))
        commands.append(command.format(**env))
        plugins.append(plugin_generator if not callable(plugin_generator) else plugin_generator(command, env))
    return commands, plugins


def exec_single(command, variables={ }, run=True):
    """
    Method will create executor object and execute it is desired
    :param command:
    :return:
    """
    ex = Executor(command.format(**variables), [PluginEnv(variables)])
    if run:
        ex.run()
    return ex


def exec_all(command, variables={ }, plugin_generator=[], run=True):
    """
    Method which will return list of executors for every combination of variables
    :param command:
    :param variables:
    :param plugin_generator:
    :return:
    """
    commands, plugins = expand_command(
        command,
        expand_vars(variables) if type(variables) is list else variables,
        plugin_generator)

    result = []
    for i in range(len(commands)):
        ex = Executor(commands[i], plugins[i])
        result.append(ex.run() if run else ex)
    return result

#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs

import platform
from subprocess import check_output
import re
from copy import copy as shallowcopy
import sys

from flowrunner.runner.execution.plugins.plugin_env import PluginEnv
from flowrunner.runner.execution.plugins.plugin_json import PluginJson
from flowrunner.runner.execution.utils import exec_util

from psutil import cpu_count
from psutil import virtual_memory

bin_version_flag = {
    'java': '-version'
}

bin_version_regexp = {
    '': r'(\d+\.\d+\.\d+\.\d+|\d+\.\d+\.[0-9_]+|\d+\.\d+)'
}


def get_binary_info():
    def plugins(command, env):
        return [
            # PluginPrint(debug=False),
            # PluginWrite(stdout='foo.log'.format(**env), stderr='bar.log'),
            # PluginProgress(name=str(env) if env else command),
            # PluginProgress(name=command.format(**env)),
            PluginJson(details={'bin': "{bin}".format(**env)}),
            PluginEnv(env=shallowcopy(env))
        ]

    #
    # exec_util.exec_all(command, options.variables, plugins)
    info = dict()
    variables = ['bin:git g++ gcc python java mono perl fortran gfortran make cmake']
    which_cmd = 'where "{bin}"' if platform.system() == "Windows" else 'which "{bin}"'
    for executor in exec_util.exec_all(which_cmd, variables, plugins):

        # grab environment
        env = executor.plugins.get('PluginEnv').env
        bin_name = env['bin']

        # clean up json
        json = shallowcopy(executor.plugins.get('PluginJson').json)
        json['path'] = ''.join(json['stdout']).strip()
        del json['stdout']
        del json['stderr']
        del json['command']
        del json['exit_code']

        # try to get more info about binary
        env['version'] = bin_version_flag.get(bin_name, '--version')
        result = exec_util.exec_all('{bin} {version}'.format(**env))[0]
        output = ' '.join(result.stderr + result.stdout).replace('\n', ' ')
        results = re.findall(bin_version_regexp.get(bin_name, bin_version_regexp['']), output)

        # some --version return non zero exit code
        if not results:
            if not json['path']:
                json['missing'] = True
                del json['path']
        else:
            json['version'] = results[0]

        info[bin_name] = json

    return info


def get_arch_info():
    info = dict()
    info['memory'] = dict()
    info['memory']['total'] = virtual_memory().total
    info['memory']['avail'] = virtual_memory().available

    # info['disk'] = [psutil.disk_partitions()]
    info['cpu'] = dict()
    info['cpu']['x64'] = sys.maxsize > 2 ** 32
    info['cpu']['physical'] = cpu_count(logical=False)
    info['cpu']['logical'] = cpu_count(logical=True)
    info['cpu']['architecture'] = platform.processor()
    if platform.system() == 'Linux':
        cpu_info = check_output('cat /proc/cpuinfo', shell=True).split('\n')
        for line in cpu_info:
            if "model name" in line:
                info['cpu']['name'] = re.sub(".*model name.*:", "", line, 1).strip()
            if "cpu MHz" in line:
                info['cpu']['frequency'] = float(re.sub(".*cpu MHz.*:", "", line, 1).strip())

    elif platform.system() == 'Windows':
        cpu_freq = check_output('wmic cpu get MaxClockSpeed', shell=True)
        cpu_freq = cpu_freq.replace('\n', '').replace('MaxClockSpeed', '').strip()
        info['cpu']['frequency'] = int(cpu_freq)

        cpu_name = check_output('wmic cpu get Caption', shell=True)
        cpu_name = cpu_name.replace('\n', '').replace('Caption', '').strip()
        info['cpu']['name'] = cpu_name

    info['system'] = dict()
    info['system']['platform'] = platform.system()
    info['system']['processor'] = platform.processor()
    info['system']['version'] = platform.version()
    info['system']['machine'] = platform.machine()
    info['system']['node'] = platform.node()
    info['system']['release'] = platform.release()

    return info

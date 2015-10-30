#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs
import platform

from subprocess import check_output
from collections import namedtuple

from flowrunner.utils.strings import extract_number


def cpu_count(logical=True):
    if platform.system() == 'Linux':
        return int(check_output('nproc', shell=True).strip())
    elif platform.system() == 'Windows':
        return int(get_windows_properties('NumberOfCores' if not logical else 'NumberOfLogicalProcessors'))


def virtual_memory():
    """
    Returns named tuple with total and available memory in MB
    :return:
    """
    info = namedtuple('memory', ['available', 'total'])
    if platform.system() == 'Linux':
        memory_info = check_output('cat /proc/meminfo', shell=True).strip()
        return info(
            long(extract_number(memory_info, 'MemFree') / 1024),
            long(extract_number(memory_info, 'MemTotal') / 1024)
        )
    elif platform.system() == 'Windows':
        return info(
            long(get_windows_properties('Capacity', 'memorychip')) / 1024,
            long(get_windows_properties('Capacity', 'memorychip')) / 1024
        )


def get_windows_properties(props=[], cls="cpu"):
    p = props if type(props) is list else [props]
    command = "wmic {cls} get {lst} /format:list".format(cls=cls, lst=','.join(p))
    output = check_output(command, shell=True).strip().split("\n")
    result = {item.split("=", 2)[0]: item.split("=", 2)[1] for item in output}

    return result.values()[0] if len(result) == 1 else result

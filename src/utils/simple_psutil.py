#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs


from subprocess import check_output
from utils.strings import extract_number
from collections import namedtuple


def cpu_count(logical=True):
    return int(
        check_output('nproc', shell=True).strip()
    )


def virtual_memory():
    memory_info = check_output('cat /proc/meminfo', shell=True).strip()
    info = namedtuple('memory', ['available', 'total'])
    return info(
        long(extract_number(memory_info, 'MemFree') * 1024),
        long(extract_number(memory_info, 'MemTotal') * 1024)
    )
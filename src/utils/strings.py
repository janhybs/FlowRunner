#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs

import re, json


def extract_number(data, name):
    lines = data.strip().split('\n')
    for line in lines:
        if line.find(name) != -1:
            match = re.match(r'.*\D(\d+)\D*', line)
            if match:
                return float(match.group(1))


def human_readable(number, round_result=False):
    units = ['', 'k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y']

    value = number

    if value < 10:
        return str(round(value, 6))

    for unit in units:
        if value >= 1000:
            value /= 1000.0
        else:
            return "{:s} {:s}".format(str(int(round(value)) if round_result else round(value, 3)), unit).strip()


def to_json(obj, filename=None):
    result = json.dumps(obj, indent=2, sort_keys=True)
    if filename:
        with open(filename, 'w') as fp:
            fp.write(result)
    return result
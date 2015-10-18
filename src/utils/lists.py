#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs
import os


def filter(iterable, *conditions):
    if type(iterable) is list:
        lst = iterable[:]
        for condition in conditions:
            lst = [x for x in lst if condition(x)]
        return lst


def union(list_a, *lists):
    set_a = set(list_a)
    for lst in lists:
        set_a = set_a.union(set(lst))
    return list(set_a)


def prepend(lst, prefix):
    return [prefix + value for value in lst]


def prepend_path(lst, *prefix):
    return [os.path.join(*(prefix + (item,))) for item in lst]

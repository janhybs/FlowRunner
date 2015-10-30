#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs
from pluck import pluck


def merge_dict(d=dict(), *args):
    dict_copy = d.copy()
    for arg in args:
        dict_copy.update(arg)
    return dict_copy


def rget(obj, path, default=None):
    names = path.split('.')
    o = obj
    for name in names:
        if name in o:
            o = o[name]
        else:
            return default
    return o


def rpluck(obj, path):
    names = path.split('.')
    last = names[-1]
    del names[-1]

    o = rget(obj, '.'.join(names), [])
    return pluck(o, last)
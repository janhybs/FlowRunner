#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs


def merge_dict(d=dict(), *args):
    dict_copy = d.copy()
    for arg in args:
        dict_copy.update(arg)
    return dict_copy

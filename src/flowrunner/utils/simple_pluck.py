#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs


def pluck (iterable, property):
    properties = property.split('.')
    result = []

    if type (iterable) is list:
        for item in iterable:
            tmp = item
            for p in properties:
                if tmp is not None:
                    tmp = tmp.get(p, None)
            if tmp:
                result.append(tmp)
        print result

    if type (iterable) is dict:
        return pluck(iterable.values(), property)
#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs
import collections
from pluck import pluck
from flowrunner.utils import rget



def categorize(items, prop_func):
    """
    :rtype : dict
    """
    getter = prop_func if callable(prop_func) else lambda x: rget(x, prop_func, None)
    result = { }
    for item in items:
        key = getter(item)
        if key in result:
            result[key].append(item)
        else:
            result[key] = [item]
    return result


def _get_short_name(k):
    v = k.strip(',').split(',')
    return v[-1] + ('root' if not v[-1] else '')


def multi_cat(items, cats=[]):
    last_cat = cats[-1]
    del cats[-1]

    result = { }
    for item in items:
        current = result
        for cat in cats:
            key = cat(item)
            if key not in current:
                current[key] = { }
            current = current[key]

        last_key = last_cat(item)
        if last_key not in current:
            current[last_key] = []
        current[last_key].append(item)
    return result

def group_by(items, group_prop_func):
    result = { }
    grp = []
    cur_grp = None
    for item in items:
        nxt_grp = group_prop_func(item)
        if nxt_grp != cur_grp:
            if cur_grp:
                result[cur_grp] = grp
            cur_grp = nxt_grp
            grp = [item]
        else:
            grp.append(item)
    if cur_grp:
        result[cur_grp] = grp
    return result


def reduce_groups(items, reductions=[]):
    result = { }
    for key, grp in items.items():
        item = { '_id': key, '_count': len(grp) }
        for reduce_field, new_field, reduce_func in reductions:
            item[new_field] = reduce_func(pluck(grp, reduce_field))
        result[key] = item
    return result


def grouper_by_name(x):
    return x['name']


def grouper_by_name_and_cpu(x):
    return '{}{}'.format(x['name'], x['nproc'])


def grouper_by_time_frame(x):
    return _get_short_name(x['path'])


class CategoryDict(object):
    def __init__(self, items):
        self.current = None
        self.holder = dict(items if type(items) is dict else {'': items})

    def _get(self, item, keys):
        if not keys:
            return item
        return self._get(item[keys[0]], keys[1:])

    def _get_keys(self, obj, parent):
        result = []
        for key, value in obj.items():
            if isinstance(value, collections.Mapping):
                result.extend(self._get_keys(value, parent + [key]))
            else:
                result.append(parent + [key])
        return result

    def __iter__(self):
        self.keys = iter(self._get_keys(self.holder, []))
        return self

    def next(self):
        for key in self.keys:
            value = self._get(self.holder, key)
            return tuple(key), value
        raise StopIteration

# data = {
#     'aa': {
#         'aa-a': [{'foo':'bar'}, {'foo':'bara'}, {'foo':'barara'}],
#         'aa-b': [{'boo':'far'}, {'boo':'barara'}],
#         'c':{
#             'd': {'e': [{'boo':'far'}]}
#         }
#     },
#     'bb': {
#         'bb-a': [{'foo':'bar'}, {'foo':'bara'}, {'foo':'barara'}],
#         'bb-b': [{'boo':'far'}, {'boo':'barara'}],
#     }
#
# }
#
# c = CategoryDict(data)
# for cats, value in c:
#     print cats, value
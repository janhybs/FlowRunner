#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs
from itertools import combinations
from operator import itemgetter
import random
from bson import SON
from pluck import pluck
from flowrunner.db.mongo import MongoDB
from flowrunner.experiments.utils import _get_short_name, multi_cat
from flowrunner.utils import rget
from flowrunner.utils.timer import Timer

true = True


def load_data():
    mongo = MongoDB()
    cursor = mongo.collections.pts.aggregate(
        [
            { '$match': {
                'context.version': { '$exists': true },
                # 'path': ",whole-program,hc-run-simulation,tos-one-step,convection-one-step,mat-mult,",
            }
            },
            { '$project': {
                '_id': {
                    'path': '$path',
                    'nproc': '$context.nproc',
                    'problem': '$context.problem',
                    'version': { '$substr': ['$context.version', 18, 1] },
                },
                'd1': { '$multiply': ['$metrics.duration', 1000000] },
                'd2': { '$multiply': ['$metrics.duration', '$context.env.cal.cpu'] },
                'cl': { '$multiply': ['$metrics.call', 1] },
            }
            },
            { '$sort':
                  SON([
                      ('_id.path', 1),
                      ('_id.nproc', 1),
                      ('_id.problem', 1),
                      ('_id.version', 1),
                  ])
            }
        ])
    return cursor


def combine_versions(items, a, b, props=['d1']):
    results = []
    keys_a = set(items[a].keys())
    keys_b = set(items[a].keys())
    # keys_a = set(['boo', 'bar'])
    # keys_b = set(['foo', 'bar', 'hala'])
    intersected = keys_a.intersection(keys_b)
    diverse = keys_a.union(keys_b) - intersected

    if diverse:
        print 'key sets are not same! They differ at {}'.format(diverse)

    for key in intersected:
        result = { 'name': key }
        for p in props:
            val_b = [float(x) for x in pluck(items[b][key], p) if x is not None]
            val_a = [float(x) for x in pluck(items[a][key], p) if x is not None]
            if not val_a or not val_b:
                # print 'missing property on {key}'.format(key=key)
                result[p] = 1.0
            else:
                # fix calculated slow-down-factor for frame f if number of collected results differ
                # only if missing collected results are results fixing random element
                # tests MUST be the same, otherwise stretching does not make sense
                result[p] = (sum(val_b) / len(val_b)) / (sum(val_a) / len(val_a))
                # result[p] = sum(val_b) / sum(val_a)
        results.append(result)
    return results


def get_version_combination(versions, history=1):
    versions = sorted(versions)
    l = len(versions)
    for i in range(len(versions)):
        for j in range(1, history + 1):
            if i + j >= l:
                continue
            yield versions[i + 0], versions[i + j], '{}x{}'.format(versions[i + 0], versions[i + j])


def slow_down_factor(measurements, version_combination, props, top=10, limit=10, reverse=True):
    slow_down_factors = { }
    for va, vb, vab in version_combination:
        result = combine_versions(measurements, va, vb, props)
        result = sorted(result, key=itemgetter('d1'), reverse=reverse)
        for k in range(top):
            favorites = expand_path(result[k]['name'])[:-1]
            result = remove_common_prefixes(result, favorites)
        slow_down_factors[vab] = result[:limit]
    return slow_down_factors


def expand_path(path):
    path = path.strip(',')
    parts = path.split(',')
    paths = [',']
    for k in range(1, len(parts) + 1):
        paths.append(',' + ','.join(parts[:k]) + ',')
    return paths


def export(results, props):
    result = 'name\t' + '\t'.join(pluck(results, 'name')) + '\n'
    for p in props:
        result +=  p + '\t' + '\t'.join(['%1.3f' % x for x in pluck(results, p)]) + '\n'
    return result

def remove_common_prefixes(items, paths):
    paths = list(paths) if type(paths) is not list else paths
    return [x for x in items if x['name'] not in paths]


# fetch data and categorize them by version and then by time-frame path
measurements = multi_cat(load_data(), [
    lambda x: rget(x, '_id.version', None),
    # lambda x: _get_short_name(rget(x, '_id.path', None)),
    lambda x: rget(x, '_id.path', None),
])

props = ['d1', 'd2', 'cl']
version_combination = list(get_version_combination(measurements.keys(), history=2))
slow_down_factors = slow_down_factor(measurements, version_combination, props, top=10, limit=10)

clipboard_result = ''
for va, vb, vab in version_combination:
    calc_output = export(slow_down_factors[vab], props)
    print vab
    print calc_output
    clipboard_result += calc_output


import pyperclip
pyperclip.copy(clipboard_result)
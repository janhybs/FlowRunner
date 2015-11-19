#!/usr/bin/python
# -*- 'coding': utf-8 -*-
# 'author':   Jan Hybs
import itertools
import math
from flowrunner.db.mongo import MongoDB, fetch_all
from flowrunner.utils import rpluck, rget
from flowrunner.utils.json_preprocessor import JsonPreprocessor
from flowrunner.utils.lists import union
from flowrunner.utils.strings import to_json
from pluck import pluck
from bson import int64, SON
import numpy as np
from operator import itemgetter

true = True
mil = 1/1000000.0
mongo = MongoDB()
cursor = mongo.collections.pts.aggregate(
    [
    { '$match': {
        'context.version': {'$exists': true},
        # 'path': ",whole-program,hc-run-simulation,tos-one-step,convection-one-step,mat-mult,",
        }
    },
    # {
    #   '$group': {
    #       '_id': {
    #           'path': '$path',
    #           'nproc': '$context.nproc',
    #           'problem': '$context.problem',
    #           'version': {'$substr': ['$context.version', 18, 1]},
    #       },
    #       'duration': {'$push': {'$multiply': ['$metrics.duration', 1000]}}
    #     }
    # },
    { '$project': {
        'duration': {'$multiply': ['$metrics.duration', 1000000]},
        '_id': {
            'path': '$path',
            'nproc': '$context.nproc',
            'problem': '$context.problem',
            'version': {'$substr': ['$context.version', 18, 1]},
            }
        }
    },
        {'$sort':
             SON([
                 ('_id.path', 1),
                 ('_id.nproc', 1),
                 ('_id.problem', 1),
                 ('_id.version', 1),
             ])
        }
    ])


aggr_result = fetch_all(cursor)

#
# def foo(x):
# if type(x) is not list:
#         return str(x)
#     return [str(i) for i in x]
#
#
# def filter(col, value, field='_id'):
#     return [element for element in col if element[field] == value]
#
#
# aggr_result = fetch_all(cursor)
#
# env_ids = pluck(aggr_result, 'environment_id')
# env_ids = union([], *env_ids)
#
# env_results = fetch_all(mongo.collections.environment.aggregate([
#     { '$match': { '_id': { '$in': env_ids } } },
#     { '$project': { '_id': 1, 'cpu': '$calibration.cpu', 'node': '$arch.system.node' } }
# ]))
#


def categorize(items, prop_func):
    """
    :rtype : dict
    """
    getter = prop_func if callable(prop_func) else lambda x: rget(x, prop_func, None)
    result = {}
    for item in items:
        key = getter(item)
        if key in result:
            result[key].append(item)
        else:
            result[key] = [item]
    return result


def multi_cat(items, cats=[]):
    last_cat = cats[-1]
    del cats[-1]

    result = {}
    for item in items:
        current = result
        for cat in cats:
            key = cat(item)
            if key not in current:
                current[key] = {}
            current = current[key]

        last_key = last_cat(item)
        if last_key not in current:
            current[last_key] = []
        current[last_key].append(item)
    return result

foo = multi_cat(aggr_result, [
    lambda x: rget(x, '_id.problem', None),
    lambda x: rget(x, '_id.path', None),
    lambda x: rget(x, '_id.nproc', None),
    lambda x: rget(x, '_id.version', None)])


difference = list()
for problem_name, problem_items in foo.items():
    # print '- %s' % problem_name
    for path_name, path_items in problem_items.items():
        # print '-- %s' % path_name
        for nproc_name, nproc_items in path_items.items():
            # print '--- %s' % nproc_name

            keys = sorted(nproc_items.keys())
            keys = ['A', 'C']
            for key_index in range(0, len(keys)-1):
                cur = nproc_items[keys[key_index]]
                nxt = nproc_items[keys[key_index+1]]

                cur_dur = float(np.mean(pluck(cur, 'duration')))
                nxt_dur = float(np.mean(pluck(nxt, 'duration')))
                diff = (nxt_dur/cur_dur*100.0) - 100.0
                difference.append({
                    'name': '{n:s}'.format(p=nproc_name, n=path_name),
                    'result': diff})
                # print '---- {:6.0f} {:6.0f} {:5.2f}'.format(cur_dur, nxt_dur, nxt_dur/cur_dur)

difference = sorted(difference, key=itemgetter('result'), reverse=True)


def _get_short_name(k):
    v = k.strip(',').split(',')
    return v[-1] + ('root' if not v[-1] else '')


def find_hotspot(samples, delta):
    diff_sample = samples[0:int(len(samples) * delta)]
    diff_sample = sorted(diff_sample, key=itemgetter('name'))
    groups = itertools.groupby(diff_sample, key=itemgetter('name'))
    hotspots = []
    for k, g in groups:
        l = list(g)
        c =float(len(l))
        sn = _get_short_name(k)
        hotspots.append({
            'name': k,
            'short_name': sn,
            'result': sum([x['result'] for x in l]),
            'count': c,
            'freq': c / len(diff_sample) * 100,
            sn: c
        })

    hotspots = sorted(hotspots, key=itemgetter('result'), reverse=True)
    return hotspots[:]
    # return [{x['short_name']:x['result']} for x in hotspots]

    print '{:120f}'.format(delta)
    for diff in hotspots[:3]:
        print '{name:120s} = {result:8.2f} ({freq:5.2f}) %'.format(**diff)
    return hotspots[:]

meas = []
names = set(_get_short_name(x) for x in pluck(difference, 'name'))
names = 'mat-mult	convection-one-step	tos-one-step	transportoperatorspliting	postprocess	hc-run-simulation	assemble-sources	convectiontransport	whole-program	gmshreader-read-mesh	root'.split()

steps = [math.pow((x+1)/100.0, 2) for x in range(0, 100, 5)]
print '\n'.join([str(x) for x in steps])
for delta in steps:
    hotspots = find_hotspot(difference, delta)
    meas.append(hotspots)

# latex output

print '\t'.join(names)
for m in meas:
    values = []
    for name in names:
        value = '0'
        for e in m:
            if e['short_name'] == name:
                value = str(e['result'])
                break
        values.append(value)
    print '\t'.join(values)


exit()
for result in aggr_result:
    _id = dict(version='?', nproc='?', node='?')
    _id.update(result['_id'])
    print '{nproc} x {problem:30s} {version}'.format(**_id)
    # print perf_result
    print result['duration']

    # for index in range(0, len(perf_result['duration'])):
    #     print '{:5.1f} {:5.1f}'.format(perf_result['duration'][index], perf_result['duration2'][index]*mil)
    # print ''
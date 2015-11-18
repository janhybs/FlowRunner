#!/usr/bin/python
# -*- 'coding': utf-8 -*-
# 'author':   Jan Hybs
import itertools
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
            for key_index in range(0, len(keys)-1):
                cur = nproc_items[keys[key_index]]
                nxt = nproc_items[keys[key_index+1]]

                cur_dur = float(np.mean(pluck(cur, 'duration')))
                nxt_dur = float(np.mean(pluck(nxt, 'duration')))
                difference.append({
                    'name': '{n:s}'.format(p=nproc_name, n=path_name),
                    'result': nxt_dur/cur_dur*100})
                # print '---- {:6.0f} {:6.0f} {:5.2f}'.format(cur_dur, nxt_dur, nxt_dur/cur_dur)

difference = sorted(difference, key=itemgetter('result'), reverse=True)


total = len(difference)
sample_size = int(total * 0.10)
diff_sample = difference[0:sample_size]
diff_sample = sorted(diff_sample, key=itemgetter('name'))

groups = itertools.groupby(diff_sample, key=itemgetter('name'))
hotspots = []
for k, g in groups:
    hotspots.append({
        'name': k,
        'result': sum([x['result'] for x in list(g)])
    })

hotspots = sorted(hotspots, key=itemgetter('result'), reverse=True)
for diff in hotspots:
    print '{name:120s} = {result:5.1f} %'.format(**diff)


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
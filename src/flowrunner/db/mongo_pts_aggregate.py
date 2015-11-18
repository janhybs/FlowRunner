#!/usr/bin/python
# -*- 'coding': utf-8 -*-
# 'author':   Jan Hybs
from flowrunner.db.mongo import MongoDB, fetch_all
from flowrunner.utils import rpluck, rget
from flowrunner.utils.json_preprocessor import JsonPreprocessor
from flowrunner.utils.lists import union
from flowrunner.utils.strings import to_json
from pluck import pluck
from bson import int64, SON

true = True
mil = 1/1000000.0
mongo = MongoDB()
cursor = mongo.collections.pts.aggregate(
    [
    { '$match': {
        'context.version': {'$exists': true},
        'path': ",whole-program,hc-run-simulation,tos-one-step,convection-one-step,mat-mult,",
        }
    },
    {
      '$group': {
          '_id': {
              'path': '$path',
              'nproc': '$context.nproc',
              'problem': '$context.problem',
              'version': {'$substr': ['$context.version', 18, 1]},
          },
          'duration': {'$push': {'$multiply': ['$metrics.duration', 1000]}}
        }
    },
    { '$project': {
        'duration': 1,
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

perf_results = fetch_all(cursor)

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
# perf_results = fetch_all(cursor)
#
# env_ids = pluck(perf_results, 'environment_id')
# env_ids = union([], *env_ids)
#
# env_results = fetch_all(mongo.collections.environment.aggregate([
#     { '$match': { '_id': { '$in': env_ids } } },
#     { '$project': { '_id': 1, 'cpu': '$calibration.cpu', 'node': '$arch.system.node' } }
# ]))
#
for perf_result in perf_results:
    _id = dict(version='?', nproc='?', node='?')
    _id.update(perf_result['_id'])
    print '{nproc} x {problem:30s} {version}'.format(**_id)
    print perf_result['duration']
    # print perf_result['duration2']

    # for index in range(0, len(perf_result['duration'])):
    #     print '{:5.1f} {:5.1f}'.format(perf_result['duration'][index], perf_result['duration2'][index]*mil)
    # print ''
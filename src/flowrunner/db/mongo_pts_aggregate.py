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

mil = 1/1000000.0
mongo = MongoDB()
cursor = mongo.collections.pts.aggregate(
    [
        # { '$project': {
        # '_id': '$_id',
        # 'exit': '$meas.metrics.exit',
        # 'duration': '$meas.metrics.duration',
        # 'problem': '$meas.context.problem'
        #     }
        # },
        {
            '$unwind': '$meas'
        },
        { '$match': {
            '_id': ','
        }
        },
        {
            '$group': {
                '_id': {
                    'path': '$_id',
                    'problem': '$meas.context.problem',
                    'nproc': '$meas.context.nproc',
                    'version': '$meas.context.version',
                    # 'node': { '$substr': ['$meas.context.env.arch.system.node', 0, 4] },
                },
                'count': { '$sum': int64.Int64(1) },
                'duration': { '$push': { '$multiply': ['$meas.metrics.duration', '$meas.context.env.cal.cpu', mil]} },
                # 'duration': { '$push': '$meas.metrics.duration' },
                # 'machine': { '$push': '$meas.context.duration' },
                # 'environment_id': { '$push': '$meas.context.environment_id' },
                # 'avgDuration': { '$avg': '$meas.metrics.duration' },
                # 'maxDuration': { '$max': '$meas.metrics.duration' },
                # 'minDuration': { '$min': '$meas.metrics.duration' },
                # //'duration': { '$push': '$duration' },
                # //'exit': { '$push': '$exit' }
            }
        },
        {
            '$project': {
                'duration': {'$pow': [5, 2]}
            }
        },
        {'$sort':
             SON([('_id.node', 1), ('_id.nproc', 1), ('_id.problem', 1)])
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
    print '{nproc} x {problem:30s} @ {node} {version}'.format(**_id)
    for index in range(0, len(perf_result['duration'])):
        print '{:5.1f} {:5.1f}'.format(perf_result['duration'][index], perf_result['duration2'][index]*mil)
    print ''
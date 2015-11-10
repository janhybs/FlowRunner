#!/usr/bin/python
# -*- 'coding': utf-8 -*-
# 'author':   Jan Hybs
from flowrunner.db.mongo import MongoDB, fetch_all
from flowrunner.utils import rpluck, rget
from flowrunner.utils.json_preprocessor import JsonPreprocessor
from flowrunner.utils.lists import union
from flowrunner.utils.strings import to_json
from pluck import pluck

mongo = MongoDB()
cursor = mongo.collections.pts.aggregate(
    [
        # { '$project': {
        # '_id': '$_id',
        # 'exit': '$meas.metrics.exit',
        # 'duration': '$meas.metrics.duration',
        #         'problem': '$meas.context.problem'
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
                },
                'duration': { '$push': '$meas.metrics.duration' },
                'machine': { '$push': '$meas.context.duration' },
                'environment_id': { '$push': '$meas.context.environment_id' },
                'avgDuration': { '$avg': '$meas.metrics.duration' },
                'maxDuration': { '$max': '$meas.metrics.duration' },
                'minDuration': { '$min': '$meas.metrics.duration' },
                # //'duration': { '$push': '$duration' },
                # //'exit': { '$push': '$exit' }
            }
        }
    ])


def foo(x):
    if type(x) is not list:
        return str(x)
    return [str(i) for i in x]


def filter(col, value, field='_id'):
    return [element for element in col if element[field] == value]


perf_results = fetch_all(cursor)

env_ids = pluck(perf_results, 'environment_id')
env_ids = union([], *env_ids)

env_results = fetch_all(mongo.collections.environment.aggregate([
    { '$match': { '_id': { '$in': env_ids } } },
    { '$project': { '_id': 1, 'cpu': '$calibration.cpu', 'node': '$arch.system.node' } }
]))

for perf_result in perf_results:
    print perf_result['_id']['problem'], perf_result['_id']['nproc'], 'x', perf_result['_id'].get('version', 'none')
    for index in range(0, len(perf_result['duration'])):
        d = perf_result['duration'][index]
        e = perf_result['environment_id'][index]
        n = filter(env_results, e)[0]
        c = (n['cpu'] / 1000000.0)
        print '{:3.0f} {:8.1f} {:8.1f} {:8.1f}'.format(d, c, (c**1.10) * d, c*d), n['node']
    print ''

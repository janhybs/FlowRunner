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
import numpy as np

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
            '_id': ',',
            'meas.context.nproc': 2,
            # 'meas.context.version': 'release_1.8.2-872-g3b91f12',
            # 'meas.context.version': 'release_1.8.2-873-g42abcb5',
            'meas.context.version': {'$in': ['release_1.8.2-873-g42abcb5', 'release_1.8.2-872-g3b91f12']},
        }
        },
        {
            '$group': {
                '_id': {
                    'path': '$_id',
                    'problem': '$meas.context.problem',
                    'nproc': '$meas.context.nproc',
                    # 'version': '$meas.context.version',
                    # 'node': { '$substr': ['$meas.context.env.arch.system.node', 0, 4] },
                },
                'count': { '$sum': int64.Int64(1) },
                'durationB': {'$push': {'$multiply': ['$meas.metrics.duration', '$meas.context.env.cal.cpu', mil]} },
                'durationA': {'$push': '$meas.metrics.duration'},
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
        # {
        #     '$project': {
        #         'duration': {'$pow': [5, 2]}
        #     }
        # },
        {'$sort':
             # SON([('_id.node', 1), ('_id.nproc', 1), ('_id.problem', 1)])
             SON([('_id.problem', 1), ('_id.nproc', 1), ])
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

nproc_map = dict(zip([1,2,3,4,6,8], range(1,7)))
problem_map = {'flow_1-8-x.con': 10, 'flow_bddc_1-8-x.con': 20, 'transportDG_1-8-x.con': 30}

import matplotlib.pyplot as plt

for perf_result in perf_results:
    _id = dict(version='?', nproc='?', node='?')
    _id.update(perf_result['_id'])
    if len(perf_result['durationA']) <= 1:
        continue
    # print '{nproc} x {problem:30s} @ {node} {version}'.format(**_id)
    # for index in range(0, len(perf_result['durationA'])):
    stdA = float(np.std(perf_result['durationA']))
    stdB = float(np.std(perf_result['durationB']))
    problems = {'flow_1-8-x.con': 'flow', 'flow_bddc_1-8-x.con': 'bddc', 'transportDG_1-8-x.con': 'transport'}
    fmt = {'stdA': stdA, 'stdB':stdB, 'imp': stdA/stdB*100, 'prob': problems[perf_result['_id']['problem']]}
    fmt.update(_id)
    # print fmt
    print "{nproc} $\\times$ {prob:10s} & {stdA:7.3f} & {stdB:7.3f} & {imp:3.0f}\\\\ \\hline".format(**fmt)
    l = len(perf_result['durationA'])
    # plt.scatter(perf_result['durationA'], range(l))
    plt.scatter([problem_map[fmt['problem']]] * l, perf_result['durationA'], marker='o', linewidths=0)
    print '\n'.join([str(x) for x in perf_result['durationB']])
    # print '{} $\\times$ {:30s} & {:7.3f} & {:7.3f} & {:7.3f}\\\\ \\hline'.format(perf_result['_id']['nproc'], perf_result['_id']['problem'], float(stdA), float(stdB), 1/float(stdB/stdA))
    #     print '{:5.1f} {:5.1f}'.format(perf_result['durationA'][index], perf_result['durationB'][index])
    # print ''
plt.show()

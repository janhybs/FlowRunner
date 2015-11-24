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
mil = 1 / 1000000.0
mongo = MongoDB()
cursor = mongo.collections.pts.aggregate(
    [
        { '$match': {
            'context.version': { '$exists': true },
            # 'path': ",whole-program,hc-run-simulation,tos-one-step,convection-one-step,mat-mult,",
        }
        },
        # {
        # '$group': {
        # '_id': {
        #           'path': '$path',
        #           'nproc': '$context.nproc',
        #           'problem': '$context.problem',
        #           'version': {'$substr': ['$context.version', 18, 1]},
        #       },
        #       'duration': {'$push': {'$multiply': ['$metrics.duration', 1000]}}
        #     }
        # },
        { '$project': {
            'duration': { '$multiply': ['$metrics.duration', 1000000] },
            '_id': {
                'path': '$path',
                'nproc': '$context.nproc',
                'problem': '$context.problem',
                'version': { '$substr': ['$context.version', 18, 1] },
            }
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

aggr_result = fetch_all(cursor)

#
# def foo(x):
# if type(x) is not list:
# return str(x)
# return [str(i) for i in x]
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





# foo = multi_cat(aggr_result, [
#     lambda x: rget(x, '_id.problem', None),
#     lambda x: rget(x, '_id.path', None),
#     lambda x: rget(x, '_id.nproc', None),
#     lambda x: rget(x, '_id.version', None)])


#
# exit()
# difference = list()
# for problem_name, problem_items in foo.items():
#     # print '- %s' % problem_name
#     for path_name, path_items in problem_items.items():
#         # print '-- %s' % path_name
#         for nproc_name, nproc_items in path_items.items():
#             # print '--- %s' % nproc_name
#
#             keys = sorted(nproc_items.keys())
#             keys = ['A', 'B']
#             for key_index in range(0, len(keys)-1):
#                 cur = nproc_items[keys[key_index]]
#                 nxt = nproc_items[keys[key_index+1]]
#
#                 cur_dur = float(np.mean(pluck(cur, 'duration')))
#                 nxt_dur = float(np.mean(pluck(nxt, 'duration')))
#                 result = sum (pluck(nxt, 'duration')) / sum(pluck(cur, 'duration'))
#                 # diff = (nxt_dur/cur_dur*100.0) - 100.0
#                 diff = (nxt_dur / cur_dur - 0.0) * 1.0
#                 difference.append({
#                     'name': path_name,
#                     'nproc': str(nproc_name),
#                     'problem': problem_name,
#                     'time_frame': _get_short_name(path_name),
#                     'result': result
#                 })
#                 # print '---- {:6.0f} {:6.0f} {:5.2f}'.format(cur_dur, nxt_dur, nxt_dur/cur_dur)




#
# def detect_hostspot(slowdown_factors, epsilon=0.1):
#     partial_sample = slowdown_factors[0:int(len(slowdown_factors) * epsilon)]
#     partial_sample = sorted(partial_sample, key=grouper)
#
#     grouped_factors = group_by(partial_sample, grouper)
#     reducted_factors = reduce_groups(grouped_factors, [
#         ('time_frame', 'time_frame', lambda x: x[0]),
#         ('result', 'result', sum),
#         ('result', 'weighted_result', lambda x: (int(sum(x) / len(x) * 10000)) / 100.0),
#         ('nproc', 'nprocs', lambda _: _),
#     ])
#     hotspots = sorted(reducted_factors.values(), key=itemgetter('weighted_result'), reverse=True)
#     # hotspots = hotspots[:10]
#     # print '\n'.join(str(x) for x in hotspots)
#     # print pluck(hotspots, 'time_frame')
#     # print pluck(hotspots, 'weighted_result')
#     return hotspots
#
#
# versions = multi_cat(aggr_result, [
#     # lambda x: rget(x, '_id.problem', None),
#     lambda x: rget(x, '_id.version', None),
#     lambda x: _get_short_name(rget(x, '_id.path', None)),
#     # lambda x: rget(x, '_id.nproc', None),
#
# ])
#
#
# # time_frames = group_by(versions, grouper_by_time_frame)
# for version_name, version_items in versions.items():
#     for time_frame_name, time_frame_items in version_items.items():
#         versions[version_name][time_frame_name] = sum(pluck(time_frame_items, 'duration'))
#
# version_A = 'A'
# version_B = 'B'
#
# versions['AB'] = { }
# for time_frame_name, time_frame_value in versions[version_A].items():
#     versions['AB'][time_frame_name] = versions[version_B][time_frame_name] / versions[version_A][time_frame_name]
#
# slow_down_list = []
# for time_frame_name, time_frame_value in versions['AB'].items():
#     slow_down_list.append({ 'name': time_frame_name, 'slow_down_factor': time_frame_value })
#
# n = 5
# slow_down_list = sorted(slow_down_list, key=itemgetter('slow_down_factor'), reverse=True)
# print '\\textbf{time-frame}&' + '&'.join(pluck(slow_down_list[:n], 'name')) + '\\\\ \\hline'
# print '$SF_{ij}$&' + '&'.join(
#     ['%1.2f' % (x * 100) for x in pluck(slow_down_list[:n], 'slow_down_factor')]) + '\\\\ \\hline'
#
# # slow_down = reduce_groups(time_frames, [
# #     ('duration', 'slow_down', sum)
# # ])
# # print slow_down
# #
# grouper = group_by_name
# difference = sorted(difference, key=itemgetter('result'), reverse=True)
#
#
# hotspots_measurements = []
# hotspots_list = []
# epsilons = [math.pow((x+1)/100.0, 2) for x in range(0, 106, 3)]
# for epsilon in epsilons:
#     # print str(epsilon).replace('.', '.')
#     hotspots = detect_hostspot(difference, epsilon)
#     # print epsilon
#     # print pluck(hotspots[:8], 'time_frame')
#     # print pluck(hotspots[:8], 'weighted_result')
#     hotspots_measurements.append(hotspots)
#     hotspots_list.extend(hotspots)
#
# meas_groups = group_by(hotspots_list, itemgetter('time_frame'))
# meas_groups = reduce_groups(meas_groups, [('weighted_result', 'result', sum)])
# meas_groups = sorted(meas_groups.values(), key=itemgetter('result'), reverse=True)
# names = pluck(meas_groups, '_id')[:13]
#
# print '\t'.join(names).replace('convectiontransport', 'convection-transport')\
#     .replace('transportoperatorspliting', 'transport-operator-spliting')
# for m in hotspots_measurements:
#     values = []
#     for name in names:
#         value = '0'
#         for e in m:
#             if e['time_frame'] == name:
#                 value = str(e['result'])
#                 break
#         values.append(value)
#     print '\t'.join(values).replace('.', '.')


# overall_performance_drop = detect_hostspot(difference, 1)[:6]
# print '&'.join(pluck (overall_performance_drop, 'time_frame'))+'\\\\ \\hline'
# print '&'.join([str(x) for x in pluck (overall_performance_drop, 'weighted_result')])+'\\\\ \\hline'

# print meas_groups
exit(0)





# exit(0)
# meas = []
# steps = [math.pow((x+1)/100.0, 2) for x in range(0, 100, 5)]
# print '\n'.join([str(x) for x in steps])
# for delta in steps:
#     hotspots = find_hotspot(difference, delta)
#     meas.append(hotspots)
#
# # latex output
#
# names = set(_get_short_name(x) for x in pluck(difference, 'name'))
# names = 'mat-mult	convection-one-step	tos-one-step	transportoperatorspliting	postprocess	hc-run-simulation	assemble-sources	convectiontransport	whole-program	gmshreader-read-mesh	root'.split()
#
#
# print '\t'.join(names)
# for m in meas:
#     values = []
#     for name in names:
#         value = '0'
#         for e in m:
#             if e['short_name'] == name:
#                 value = str(e['result'])
#                 break
#         values.append(value)
#     print '\t'.join(values)
#
#
# exit()
# for result in aggr_result:
#     _id = dict(version='?', nproc='?', node='?')
#     _id.update(result['_id'])
#     print '{nproc} x {problem:30s} {version}'.format(**_id)
#     # print perf_result
#     print result['duration']
#
#     # for index in range(0, len(perf_result['duration'])):
#     #     print '{:5.1f} {:5.1f}'.format(perf_result['duration'][index], perf_result['duration2'][index]*mil)
#     # print ''
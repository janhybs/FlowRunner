var result = db.pts.aggregate([
{$match: {}},
{$group: {_id: '$path', contexts: {$push: "$meas.context"}}}
]).result

result

db.environment.find({}, {_id: 0, calibration: 1, 'arch.system.node': 1})
db.environment.aggregate([{$project: {_id: 0, 'cpu': '$calibration.cpu','memory': '$calibration.memory', 'node': '$arch.system.node'}}]).result
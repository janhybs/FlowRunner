var result = db.pts.aggregate([
{$match: {}},
{$group: {_id: '$path', contexts: {$push: "$meas.context"}}}
]).result

result
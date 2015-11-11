var result = db.pts.aggregate([
{$match: {}},
{$group: {_id: '$path', contexts: {$push: "$meas.context"}}}
]).result

result

db.environment.find({}, {_id: 0, calibration: 1, 'arch.system.node': 1})
db.environment.aggregate([{$project: {_id: 0, 'cpu': '$calibration.cpu','memory': '$calibration.memory', 'node': '$arch.system.node'}}]).result


var r  = db.pts.find({_id: ',', 'meas.metrics.exit': 0}, {_id: 0, 'meas.metrics.duration': 1, 'meas.context.problem': 1})
db.pts.aggregate(
[
    /*{ $project: {
            _id: '$_id',
            'exit': '$meas.metrics.exit',
            'duration': '$meas.metrics.duration',
            'problem': '$meas.context.problem'
        }
    },*/
    {
        $unwind: '$meas'
    },
    { $match: {
            _id: ','
        }
    },
    {
        $group: {
            _id: {
                path: '$_id',
                problem: '$meas.context.problem',
                nproc: '$meas.context.nproc'
            },
            duration: { $push: '$meas.metrics.duration' },
            avgDuration: { $avg: '$meas.metrics.duration' },
            maxDuration: { $max: '$meas.metrics.duration' },
            minDuration: { $min: '$meas.metrics.duration' },
            //duration: { $push: '$duration' },
            //exit: { $push: '$exit' }
        }
    }
]).result

db.pts.aggregate(
[
    /*{ $project: {
            _id: '$_id',
            'exit': '$meas.metrics.exit',
            'duration': '$meas.metrics.duration',
            'problem': '$meas.context.problem'
        }
    },*/
    {
        $unwind: '$meas'
    },
    { $match: {
            _id: ','
        }
    },
    {
        $group: {
            _id: {
                path: '$_id',
                problem: '$meas.context.problem',
                nproc: '$meas.context.nproc'
            },
            duration: { $push: '$meas.metrics.duration' },
            environment_id : { $push: '$meas.context.environment_id'},
            avgDuration: { $avg: '$meas.metrics.duration' },
            maxDuration: { $max: '$meas.metrics.duration' },
            minDuration: { $min: '$meas.metrics.duration' },
            //duration: { $push: '$duration' },
            //exit: { $push: '$exit' }
        }
    }
]).result


db.pts.aggregate(
[
    /*{ $project: {
            _id: '$_id',
            'exit': '$meas.metrics.exit',
            'duration': '$meas.metrics.duration',
            'problem': '$meas.context.problem'
        }
    },*/
    {
        $unwind: '$meas'
    },
    { $match: {
            _id: ','
        }
    },
    {
        $group: {
            _id: {
                path: '$_id',
                problem: '$meas.context.problem',
//                nproc: '$meas.context.nproc',
                version: '$meas.context.version',
                node: { $substr: ['$meas.context.env.arch.system.node', 0, 4]}
            },
            count: { $sum: NumberInt(1) },
            /*duration: { $push: '$meas.metrics.duration' },
            environment_id : { $push: '$meas.context.environment_id'},*/
            avgDuration: { $avg: '$meas.metrics.duration' },
            maxDuration: { $max: '$meas.metrics.duration' },
            minDuration: { $min: '$meas.metrics.duration' },
            //duration: { $push: '$duration' },
            //exit: { $push: '$exit' }
        }
    }
]).result

db.pts.aggregate(
[
    /*{ $project: {
            _id: '$_id',
            'exit': '$meas.metrics.exit',
            'duration': '$meas.metrics.duration',
            'problem': '$meas.context.problem'
        }
    },*/
    {
        $unwind: '$meas'
    },
    { $match: {
            _id: ','
        }
    },
    {
        $group: {
            _id: {
                path: '$_id',
                problem: '$meas.context.problem',
//                nproc: '$meas.context.nproc',
                version: '$meas.context.version',
                node: { $substr: ['$meas.context.env.arch.system.node', 0, 4]}
            },
            count: { $sum: NumberInt(1) },
            duration: { $push: { $multiply: ['$meas.metrics.duration', '$meas.context.env.cal.cpu', 1.0 / 1000000]} },
            /*duration: { $push: '$meas.metrics.duration' },
            environment_id : { $push: '$meas.context.environment_id'},*/
            /*avgDuration: { $avg: '$meas.metrics.duration' },
            maxDuration: { $max: '$meas.metrics.duration' },
            minDuration: { $min: '$meas.metrics.duration' },*/
            //duration: { $push: '$duration' },
            //exit: { $push: '$exit' }
        }
    }
]).result


db.pts.aggregate(
[
    /*{ $project: {
            _id: '$_id',
            'exit': '$meas.metrics.exit',
            'duration': '$meas.metrics.duration',
            'problem': '$meas.context.problem'
        }
    },*/
    {
        $unwind: '$meas'
    },
    { $match: {
            _id: ','
        }
    },
    {
        $group: {
            _id: {
                path: '$_id',
                problem: '$meas.context.problem',
                nproc: '$meas.context.nproc',
                version: '$meas.context.version',
                node: { $substr: ['$meas.context.env.arch.system.node', 0, 4]}
            },
            count: { $sum: NumberInt(1) },
            duration: { $push: { $multiply: ['$meas.metrics.duration', '$meas.context.env.cal.cpu', 1.0 / 1000000]} },
        }
    },
    { $project: { raisedTo2: { $pow: [ 5, 2 ] } } },
    {
        $sort: {
            '_id.nproc': 1,
            '_id.problem': 1
        }
    }
]).result
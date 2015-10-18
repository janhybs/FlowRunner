#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs
import time

from pbs.script import PBSScript

details = {
    'name': 'flow-and-env',
    'limits': {
        'walltime': '01:30:00',
        'mem': "4gb",
        'nodes': '1:ppn=4',  #:infiniband
        'scratch': '1gb'
    },
    'flags': {
    },
    'modules': [
        'cmake-2.8',
        'python-2.7.6-gcc',  # python-2.7.10-gcc
        'gcc-4.7.0',  # gcc-4.8.1 gcc-4.8.4 gcc-4.5.2
        'openmpi',
        'perl-5.10.1',
        'boost-1.49',  # boost-1.55
        'python26-modules-gcc',
        'numpy-py2.6'
    ],
    # additional
    'join_output': True,
    'mail_result': 'abe'
}

execution_section = """

DATADIR="$PBS_O_WORKDIR"

echo $SCRATCHDIR
cd $SCRATCHDIR || exit 2

pwd
whoami
nproc
gcc --version


mkdir FlowRunner
cd FlowRunner
git clone https://github.com/x3mSpeedy/FlowRunner.git
cd FlowRunner/src
rm performance.json || echo "no such file"
python performance.py -c 1 -c 2 -c 3 -c 4 -x "matrix-creation" -x "matrix-solve" -x "_matrix-solve" -x "_matrix-creation"

cp performance.json $DATADIR || export CLEAN_SCRATCH=false



cd $SCRATCHDIR || exit 2
mkdir Flow123d
cd Flow123d
git clone https://github.com/flow123d/flow123d.git
cd flow123d
cp config/config-jenkins-linux-debug.cmake config.cmake
cmake . > flow123d-build.log 2>&1
cp flow123d-build.log $DATADIR || export CLEAN_SCRATCH=false


cd $SCRATCHDIR || exit 2
rm -rf Flow123d
rm -rf FlowRunner

"""


script = PBSScript()
script.header(details)
script.add_file('work.sh')
script.save('pbs-script.sh')
# script.start_job()
# script.wait_for_exit()

#
# content = PBSScript.build(details)
# content += execution_section
#
# print '-' * 100
# print content
# print '-' * 100
#
# filename = 'foo.sh'
# PBSScript.save_to_file(content, filename)
# job = PBSScript.run_job(filename)
# print PBSScript.wait_for_exit(job, 5)
#

#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs

from pbs.script import PBSScript

details = {
    'name': 'simple-test-job',
    'limits': {
        'walltime': '00:05:00',
        'mem': "200mb",
        'nodes': '1:ppn=1',  #:infiniband
        'scratch': '400mb'
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

# nastaveni uklidu SCRATCHE pri chybe nebo ukonceni
# (pokud nerekneme jinak, uklidime po sobe)
trap 'clean_scratch' TERM EXIT

DATADIR="/storage/praha1/home/$LOGNAME/" # sdilene pres NFSv4

cp $DATADIR/vstup.txt $SCRATCHDIR  || exit 1
cd $SCRATCHDIR || exit 2

pwd
whoami
nproc
cat vstup.txt
cat vstup.txt > vystup.txt
cat vstup.txt >> vystup.txt
python -V
gcc --version

cp vystup.txt $DATADIR || export CLEAN_SCRATCH=false
"""


content = PBSScript.build(details)
content += execution_section

print '-' * 100
print content
print '-' * 100

filename = 'foo.sh'
PBSScript.save_to_file(content, filename)
job = PBSScript.run_job(filename)
print PBSScript.wait_for_exit(job, 5)


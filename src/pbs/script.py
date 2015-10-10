#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs
import re
import subprocess
import time
from pbs.job import Job, JobState


class PBSScript(object):
    @staticmethod
    def build(details={ }):
        limits = details.get('limits', { })
        flags = details.get('flags', { })
        modules = details.get('modules', [])
        job_name = details.get('name', 'test-job')
        join_output = details.get('join_output', False)
        mail_result = details.get('mail_result', '')
        # mail -m a(aborts), b(begins), e(end)
        # join -j oe (out, err)

        if '/software/modules/current/metabase' not in modules:
            modules = ['/software/modules/current/metabase'] + modules

        pbs = list()
        pbs.append('#!/bin/bash')
        pbs.append('#PBS -N {name}'.format(name=job_name))

        for limit_name, limit_value in limits.items():
            pbs.append('#PBS -l {name}={value}'.format(name=limit_name, value=limit_value))

        for flag_name, flag_value in flags.items():
            pbs.append('#PBS -{name} {value}'.format(name=flag_name, value=flag_value))

        if join_output:
            pbs.append('#PBS -j oe')

        if mail_result:
            pbs.append('#PBS -m {value}'.format(value=mail_result if type(mail_result) is str else 'abe'))

        pbs.append('#')
        pbs.append('')
        pbs.append('module purge')

        for module in modules:
            pbs.append('module add {name}'.format(name=module))

        return '\n'.join(pbs)

    @staticmethod
    def save_to_file(content, filename='test-script.sh'):
        with open(filename, 'w') as fp:
            fp.write(content)

    @staticmethod
    def run_job (filename):
        # run qsub and get job id
        output = subprocess.check_output(['qsub', filename]).strip()
        job_id = re.match(r'(\d+)', output).group(1)

        # create job and periodically test job end
        return Job(job_id)

    @staticmethod
    def wait_for_exit (job, sleep_time=60):
        print job
        while job.state != JobState.COMPLETED:
            job.fetch_info()
            print job
            time.sleep(sleep_time)
        return job
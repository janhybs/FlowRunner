#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs
import os
import re
import subprocess
import time

from flowrunner.pbs.job import Job, JobState


class PBSScript(object):
    def __init__(self, output=None):
        self.files = list()
        self.content = ""
        self.details = { }
        self.output = output
        self.job = None
        self.definitions = {}

    def add_file(self, filename):
        self.files.append(filename)

    def peek(self):
        """
        Return cmd command which will reserve system with specified resources
        :return:
        """
        limits = ' '.join(["-l {n}={v}".format(n=n, v=v) for n,v in self.details.get("limits", {}).items()])
        return "qsub -I {limits}".format(limits = limits).strip()

    def save(self, output='pbs-script.sh'):
        self.content = self.build(self.details)
        self.content += "\n\n"
        for name, value in self.definitions.items():
            bash_name = str(name).upper().replace(".", '_')
            self.content += """{bash_name}="{value}"\n""".format(bash_name=bash_name, value=value)

        for file in self.files:
            with open(file, 'r') as fp:
                self.content += '\n' + fp.read()
        if output:
            self.output = output
            with open(output, 'w+') as fp:
                fp.write(self.content)
                fp.flush()
                fp.close()
        else:
            print self.content
        return self.content

    def header(self, details):
        self.details = details

    def build(self, details={ }):
        limits = details.get('limits', { })
        flags = details.get('flags', { })
        modules = details.get('modules', [])
        job_name = details.get('name', 'test-job')
        join_output = details.get('join_output', False)
        mail_result = details.get('mail_result', '')
        self.details = details
        # mail -m a(aborts), b(begins), e(end)
        # join -j oe (out, err)

        if '/software/modules/current/metabase' not in modules:
            modules = ['/software/modules/current/metabase'] + modules

        pbs = list()
        pbs.append('#!/bin/bash')
        pbs.append('#PBS -N {name}'.format(name=job_name))

        for limit_name, limit_value in limits.items():
            pbs.append('#PBS -l {name}={value}'.format(name=limit_name, value=limit_value))

            if limit_name == 'nodes':
                self.definitions['cpu.arch.avail'] = str(limit_value).split(':')[0]

            if limit_name == 'mem':
                self.definitions['cpu.memory.avail'] = str(limit_value)

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

        pbs.append('')
        return '\n'.join(pbs)

    def start_job(self):
        # run qsub and get job id

        if not os.path.exists(self.output):
            raise "File {} does not exist".format(self.output)

        output = subprocess.check_output(['qsub', self.output]).strip()
        job_id = re.match(r'(\d+)', output).group(1)

        # create job and periodically test job end
        self.job = Job(job_id)
        print self.job
        return self.job

    def wait_for_exit(self, sleep_time=60):
        print self.job
        while self.job.state != JobState.COMPLETED:
            self.job.fetch_info()
            print self.job
            time.sleep(sleep_time)
        return self.job

#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs

from copy import copy as shallowcopy
import os
from os.path import join as join_path
import re
from shutil import rmtree, copyfile
from pluck import pluck
import shutil
from runner.execution.plugins.plugin_env import PluginEnv
from runner.execution.plugins.plugin_json import PluginJson
from runner.execution.plugins.plugin_progress import PluginProgress
from runner.execution.plugins.plugin_timer import PluginTimer
from runner.execution.utils.exec_util import check_output_secure, exec_all, exec_single
from utils.io import browse, mkdir, strip_ext
import utils.lists
from utils.strings import to_json


class FlowTester(object):
    def __init__(self, **kwargs):
        self.tests_root = os.path.abspath(kwargs.get('test_root'))
        self.output_dir = os.path.abspath(join_path(self.tests_root, kwargs.get('tests_output', '_output')))
        self.select_dir_rule = re.compile(kwargs.get('select_dir_rule', r'\d+_.*'))
        self.select_ini_rule = re.compile(kwargs.get('select_ini_rule', r'.*'))
        self.select_artifact_rule = re.compile(kwargs.get('select_artifact_rule', r'.*/profiler.*\.json$'))
        self.bins = {
            "flow123d": kwargs.get("flow123d"),
            "mpiexec": kwargs.get("mpiexec"),
            "ndiff": kwargs.get("ndiff")
        }

        self.all_tests = sorted([test for test in os.listdir(self.tests_root)])

        # filter folders
        self.all_tests = utils.lists.filter(self.all_tests, lambda x: os.path.isdir(join_path(self.tests_root, x)))
        self.selected_tests = utils.lists.filter(self.all_tests, lambda x: self.select_dir_rule.match(x))
        self.tests = { test: self.test_template() for test in self.selected_tests }


    def run(self):
        for test_name, test_option in self.tests.items():
            cwd = join_path(self.tests_root, test_name)
            cons = check_output_secure('ls *.con', cwd=cwd).strip().split()
            yamls = check_output_secure('ls *.yaml', cwd=cwd).strip().split()

            test_option['problem'] = utils.lists.union(cons, yamls)
            test_option['problem'] = utils.lists.filter(test_option['problem'], lambda x: bool(x))
            test_option['problem'] = utils.lists.filter(test_option['problem'], lambda x: self.select_ini_rule.match(x))

            test_option['input_path'] = join_path(self.tests_root, test_name, test_option['input'])
            test_option['output_path'] = join_path(self.tests_root, test_name, test_option['output'])
            test_option['ref_output_path'] = join_path(self.tests_root, test_name, test_option['ref_output'])
            test_option['problem_config'] = utils.lists.prepend_path(test_option['problem'], self.tests_root, test_name)

            def plugins(command, env):
                return [
                    # PluginPrint(debug=False),
                    # PluginWrite(stdout='foo.log'.format(**env), stderr='bar.log'),
                    # PluginProgress(name=str(env) if env else command),
                    PluginProgress(name=command.format(**env)),
                    PluginJson(details={ 'problem_config': "{problem_config}".format(**env) }),
                    PluginEnv(env=shallowcopy(env)),
                    PluginTimer()
                ]

            # prepare all executors
            executors = exec_all(
                "{mpiexec} -np {nproc} {flow123d} -s {problem_config} -i {input_path} -o {output_path}",
                {
                    'flow123d': self.bins['flow123d'],
                    'mpiexec': self.bins['mpiexec'],
                    'problem_config': test_option['problem_config'],
                    'input_path': test_option['input_path'],
                    'output_path': test_option['output_path'],
                    'ref_output_path': test_option['ref_output_path'],
                    'test': test_name,
                    'nproc': test_option['nproc'],
                    'info_json': test_option['info_json']
                }, plugins, run=False
            )

            for executor in executors:
                env = executor.environment

                # purge output directory
                if os.path.exists(env['output_path']):
                    rmtree(env['output_path'])

                # run test
                executor.run()

                # locate ref output dir
                ini = os.path.basename(env['problem_config'])
                ref_dir = join_path(env['ref_output_path'], ini)
                output_dir = env['output_path']

                # grab all files in dir
                files_to_compare = browse(ref_dir)
                files_to_compare = [file.replace(ref_dir, '').lstrip('/\\') for file in files_to_compare]

                # compare them
                comparisons = []
                for filename in files_to_compare:
                    comparison = exec_single(
                        """{ndiff} "{ref}" "{res}" """, {
                            'ndiff': self.bins['ndiff'],
                            'ref': join_path(ref_dir, filename),
                            'res': join_path(output_dir, filename),
                            'file': filename
                        }
                    )
                    comparisons.append(comparison)

                # save info about test
                info = dict()
                info['exit'] = executor.exit_code
                info['nproc'] = executor.environment['nproc']
                info['test'] = executor.environment['test']
                info['problem'] = os.path.basename(executor.environment['problem_config'])
                info['nproc'] = env['nproc']
                info['duration'] = executor.plugins.get('PluginTimer').duration

                if max(pluck(comparisons, 'exit_code')) == 0:
                    info['correct'] = True
                    # info['comparisons'] = []
                else:
                    info['correct'] = False
                    info['comparisons'] = [ex.environment['file'] for ex in comparisons if ex.exit_code != 0]

                if executor.exit_code != 0:
                    e = '\n'.join(executor.stderr)
                    i = e.lower().find('error')
                    info['stderr'] = e[i - 100: i + 1024]

                info_json =  executor.environment['info_json'].format(**info)
                info_json = join_path(self.output_dir, info_json)
                mkdir(info_json, is_file=True)
                to_json(info, info_json)

                # grab profiler
                profilers = browse(env['output_path'])
                profilers = utils.lists.filter(profilers, lambda x: self.select_artifact_rule.match(x))

                counter = 1
                for profiler in profilers:
                    path = join_path(self.output_dir, "{info_json}.profiler-{counter}.json".format(info_json=strip_ext(info_json), counter=counter))
                    mkdir(path, is_file=True)
                    shutil.move(profiler, path)
                    counter += 1

    def test_template(self):
        return {
            'ini': [], 'nproc': [1,2,3], 'input': 'input', 'output': 'output', 'ref_output': 'ref_output',
            'info_json': "{test}/{problem}/info-{nproc}.json"
        }
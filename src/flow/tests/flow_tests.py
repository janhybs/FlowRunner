#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs

from copy import copy as shallowcopy
import os
import re
from shutil import rmtree, copyfile
import shutil
import datetime
from runner.execution.plugins.plugin_brief_info import PluginBriefInfo
from runner.execution.plugins.plugin_env import PluginEnv
from runner.execution.plugins.plugin_json import PluginJson
from runner.execution.plugins.plugin_print import PluginPrint
from runner.execution.plugins.plugin_print_command import PluginPrintCommand
from runner.execution.plugins.plugin_progress import PluginProgress
from runner.execution.plugins.plugin_timer import PluginTimer
from runner.execution.utils.exec_util import check_output_secure, exec_all, exec_single, prepare_all, prepare_single
from utils import merge_dict
from utils.io import browse, mkdir, strip_ext
import utils.lists
from utils.pluck import pluck
from utils.strings import to_json
from utils import io


class FlowTester(object):
    def __init__(self, **kwargs):
        if kwargs.get('flow_root'):
            self.flow_root = os.path.abspath(kwargs.get('flow_root'))

        if kwargs.get('test_root'):
            self.tests_root = os.path.abspath(kwargs.get('test_root'))
        else:
            self.tests_root = io.join_path(self.flow_root, 'tests')

        self.nproc = kwargs.get('nproc', [1, 2, 3])
        self.output_dir = os.path.abspath(io.join_path(self.tests_root, kwargs.get('tests_output', '_output')))

        output_timestamp_dir = kwargs.get('output_timestamp_dir', '%Y-%m-%d_%H-%M-%S')
        if output_timestamp_dir:
            self.output_dir = io.join_path(self.output_dir, datetime.datetime.now().strftime(output_timestamp_dir))

        self.select_dir_rule = re.compile(kwargs.get('select_dir_rule', r'\d+_.*'))
        self.select_ini_rule = re.compile(kwargs.get('select_ini_rule', r'.*'))
        self.select_artifact_rule = re.compile(kwargs.get('select_artifact_rule', r'.*/profiler.*\.json$'))

        f, m, n = kwargs.get("flow123d"), kwargs.get("mpiexec"), kwargs.get("ndiff")
        self.bins = {
            "flow123d": f if f else io.join_path(self.flow_root, 'build_tree', 'bin', 'flow123d'),
            "mpiexec": m if m else io.join_path(self.flow_root, 'build_tree', 'bin', 'mpiexec'),
            "ndiff": n if n else io.join_path(self.flow_root, 'bin', 'ndiff', 'ndiff.pl')
        }

        all_tests = sorted([test for test in os.listdir(self.tests_root)])

        # filter folders
        all_tests = utils.lists.filter(all_tests, lambda x: os.path.isdir(io.join_path(self.tests_root, x)))
        selected_tests = utils.lists.filter(all_tests, lambda x: self.select_dir_rule.match(x))
        self.tests = { test: self.test_template() for test in selected_tests }

    def browse_test_config_files(self, test_name, test_option):
        # browse con and yamls files
        cwd = io.join_path(self.tests_root, test_name)
        cons = check_output_secure('ls *.con', cwd=cwd).strip().split()
        yamls = check_output_secure('ls *.yaml', cwd=cwd).strip().split()

        # union these lists and filter them
        test_option['problem'] = utils.lists.union(cons, yamls)
        test_option['problem'] = utils.lists.filter(test_option['problem'], lambda x: bool(x))
        test_option['problem'] = utils.lists.filter(test_option['problem'], lambda x: self.select_ini_rule.match(x))

    def setup_test_paths(self, test_name, test_option):
        test_option['input_path'] = io.join_path(self.tests_root, test_name, test_option['input'])
        test_option['output_path'] = io.join_path(self.tests_root, test_name, test_option['output'])
        test_option['ref_output_path'] = io.join_path(self.tests_root, test_name, test_option['ref_output'])
        test_option['problem_config'] = utils.lists.prepend_path(test_option['problem'], self.tests_root, test_name)

        del test_option['input']
        del test_option['output']
        del test_option['ref_output']
        del test_option['problem']

    def prepare_test_executor(self, test_name, test_option):
        # define plugin generator
        def plugins(command, env):
            return [
                PluginPrint(),
                PluginPrintCommand(),
                # PluginWrite(stdout='foo.log'.format(**env), stderr='bar.log'),
                # PluginProgress(name=str(env) if env else command),
                PluginProgress(name="x{nproc} {flow123d} -s {problem_config}".format(
                    nproc=env['nproc'],
                    flow123d=io.end_path(env['flow123d'], 2),
                    problem_config=io.end_path(env['problem_config'], 2),
                )),
                # PluginJson(details={ 'problem_config': "{problem_config}".format(**env) }),
                PluginEnv(env=shallowcopy(env)),
                PluginTimer()
            ]

        return prepare_all(
            command="{mpiexec} -np {nproc} {flow123d} -s {problem_config} -i {input_path} -o {output_path}",
            variables=merge_dict(self.bins, test_option, {
                'test': test_name,
            }),
            plugin_generator=plugins
        )

    def compare_results_files(self, environment):
        # locate ref output dir
        problem_config = os.path.basename(environment['problem_config'])
        ref_dir = io.join_path(environment['ref_output_path'], problem_config)
        output_dir = environment['output_path']

        # grab all files in dir
        files_to_compare = browse(ref_dir)
        files_to_compare = [f.replace(ref_dir, '').lstrip('/\\') for f in files_to_compare]

        # compare them
        comparisons = []
        for filename in files_to_compare:
            variables = {
                'ndiff': self.bins['ndiff'],
                'ref': io.join_path(ref_dir, filename),
                'res': io.join_path(output_dir, filename),
                'file': filename,
                'name': "comparison {file}".format(file=filename)
            }
            comparison = exec_single(
                command="""perl {ndiff} "{ref}" "{res}" """,
                variables=variables,
                plugins=[
                    PluginEnv(variables),
                    PluginBriefInfo(name=variables['name'])
                ]
            )
            comparisons.append(comparison)
        return comparisons

    def run(self):
        for test_name, test_option in self.tests.items():
            self.browse_test_config_files(test_name, test_option)
            self.setup_test_paths(test_name, test_option)
            executors = self.prepare_test_executor(test_name, test_option)

            for executor in executors:
                environment = executor.environment

                # purge output directory
                if os.path.exists(environment['output_path']):
                    rmtree(environment['output_path'])

                # run test
                executor.run()

                # get comparisons
                comparisons = self.compare_results_files(environment)

                # save info about test
                info = dict()
                info['exit'] = executor.exit_code
                info['nproc'] = executor.environment['nproc']
                info['test'] = executor.environment['test']
                info['problem'] = os.path.basename(executor.environment['problem_config'])
                info['nproc'] = environment['nproc']
                info['duration'] = executor.plugins.get('PluginTimer').duration
                info['path'] = "{r}/{e[test]}/{i[problem]}".format(
                    r=io.relative(self.flow_root, self.tests_root),
                    e=executor.environment,
                    i=info
                )
                info['root'] = self.flow_root

                if not comparisons or max(pluck(comparisons, 'exit_code')) == 0:
                    info['correct'] = True
                    # info['comparisons'] = []
                else:
                    info['correct'] = False
                    info['comparisons'] = [ex.environment['file'] for ex in comparisons if ex.exit_code != 0]

                if executor.exit_code != 0:
                    # e = '\n'.join(executor.stderr)
                    # i = e.lower().find('error')
                    # info['stderr'] = e[i - 100: i + 1024]
                    info['stderr'] = executor.stderr
                info['stdout'] = executor.stdout

                info_json = executor.environment['info_json'].format(**info)
                info_json = io.join_path(self.output_dir, info_json)
                mkdir(info_json, is_file=True)
                print to_json(info, info_json)

                # grab profiler
                profilers = browse(environment['output_path'])
                profilers = utils.lists.filter(profilers, lambda x: self.select_artifact_rule.match(x))

                counter = 1
                for profiler in profilers:
                    path = io.join_path(self.output_dir,
                                     "{info_json}.profiler-{counter}.json".format(
                                         info_json=strip_ext(info_json),
                                         counter=counter))
                    mkdir(path, is_file=True)
                    shutil.move(profiler, path)
                    counter += 1

    def test_template(self):
        return {
            'nproc': self.nproc, 'input': 'input', 'output': 'output', 'ref_output': 'ref_output',
            'info_json': "{test}/{problem}/info-{nproc}.json"
        }
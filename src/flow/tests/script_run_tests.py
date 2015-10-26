#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs

import sys, os
sys.path.append(os.getcwd())

from system import python
python.init()

from utils.strings import to_json
from utils.parser import Parser
from flow.tests.flow_tests import FlowTester



def create_parser():
    """Creates command line parse"""

    # defaults
    flow_root = '/home/jan-hybs/Documents/Flow123d/flow123d'
    p = Parser()

    p.add("r test-root", "test_root", help="Test root location or --flow-root")
    p.add("t flow-root", "flow_root", default=flow_root, help="Flow root folder")
    p.add("m mpiexec", "mpiexec", help="MPI exec location or --flow-root")
    p.add("f flow123d", "flow123d", help="Flow123d bin location or --flow-root")
    p.add("d ndiff", "ndiff", help="Ndiff utility location or --flow-root")
    p.add("n nproc", "nproc", help="Nproc number", default=[], expand=True, type='int')
    p.add("o tests-output", "tests_output", default='__output', help="Output folder where files will be stored")
    p.add("  select-dir-rule", "select_dir_rule", default=r'\d+_.*', help="RegExp for tests directory")
    p.add("  select-ini-rule", "select_ini_rule", default=r'.*', help="RegExp for tests subdirs")
    p.add("  select-artifact-rule", "select_artifact_rule", default=r'.*/profiler.*\.json$', help="RegExp for artifact files")
    p.add("  output-timestamp-dir", "output_timestamp_dir", default='%Y-%m-%d_%H-%M-%S', help="Additional timestamp dir format")

    p.set_usage("""%prog [options]""")
    p.check_args = check_args
    return p


def check_args(options, args):
    """Parses argument using given parses and check resulting value combination"""
    if not options.nproc:
        options.nproc = [1, 2, 3, 4]

    options.nproc = [int(v) for v in options.nproc]

    # convert to int
    return options, args,


def main():
    options, args = create_parser().parse()

    print 'Settings: '
    print to_json(options.__dict__)

    tester = FlowTester(**options.__dict__)
    tester.run()


if __name__ == '__main__':
    main()

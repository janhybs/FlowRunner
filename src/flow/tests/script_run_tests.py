#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs

import os, sys
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), 'libs'))
sys.path.append(os.path.join(os.getcwd(), 'lib'))

from flow.tests.flow_tests import FlowTester
from optparse import OptionParser



def create_parser():
    """Creates command line parse"""

    # defaults
    flow_root = '/home/jan-hybs/Dokumenty/Smartgit-flow/flow123d'

    parser = OptionParser()

    def opt (flag_format, destination, **kwargs):
        kwargs['dest'] = destination
        flags = str(flag_format).strip().split()
        flags = sorted(flags, lambda a, b: len(a) - len(b))
        if len(flags) == 1:
            flags[0] = '--' + flags[0] if len(flags[0]) > 1 else '-' + flags[0]
        else:
            flags[0], flags[1] = '-' + flags[0],  '--' + flags[1]
        parser.add_option(*flags, **kwargs)

    opt("r test-root", "test_root", help="Test root location or --flow-root")
    opt("t flow-root", "flow_root", default=flow_root, help="Flow root folder")
    opt("m mpiexec", "mpiexec", help="MPI exec location or --flow-root")
    opt("f flow123d", "flow123d", help="Flow123d bin location or --flow-root")
    opt("n ndiff", "ndiff", help="Ndiff utility location or --flow-root")
    opt("o tests-output", "tests_output", default='__output', help="Output folder where files will be stored")
    opt("  select-dir-rule", "select_dir_rule", default=r'\d+_.*', help="RegExp for tests directory")
    opt("  select-ini-rule", "select_ini_rule", default=r'.*', help="RegExp for tests subdirs")
    opt("  select-artifact-rule", "select_artifact_rule", default=r'.*/profiler.*\.json$', help="RegExp for artifact files")

    parser.set_usage("""%prog [options]""")
    return parser


def parse_args(parser):
    """Parses argument using given parses and check resulting value combination"""
    options, args = parser.parse_args()
    return options, args,


def main():
    parser = create_parser()
    options, args = parse_args(parser)
    options.select_dir_rule = r'.*'
    options.select_ini_rule = r'.*'
    # options.output_timestamp_dir = ''
    options.nproc = [1, 2, 3]
    tester = FlowTester(**options.__dict__)
    tester.run()


if __name__ == '__main__':
    main()

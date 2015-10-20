#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs

import os, sys
sys.path.append(os.getcwd())

from flow.tests.flow_tests import FlowTester



from optparse import OptionParser


def create_parser():
    # defaults
    mpiexec_bin = '/home/jan-hybs/Documents/Flow123d/flow123d/build_tree/bin/mpiexec'
    flow_bin = '/home/jan-hybs/Documents/Flow123d/flow123d/build_tree/bin/flow123d'
    ndiff = '/home/jan-hybs/Documents/Flow123d/flow123d/bin/ndiff/ndiff.pl'
    tests_output = '__output'
    root = '/home/jan-hybs/Documents/Flow123d/flow123d/tests'

    """Creates command line parse"""
    parser = OptionParser()

    parser.add_option("-r", "--test-root", dest="test_root", default=root, help="Test root location")
    parser.add_option("-m", "--mpiexec", dest="mpiexec", default=mpiexec_bin, help="MPI exec location")
    parser.add_option("-f", "--flow123d", dest="flow123d", default=flow_bin, help="Flow123d bin location")
    parser.add_option("-n", "--ndiff", dest="ndiff", default=ndiff, help="Ndiff utility location")
    parser.add_option("-o", "--tests-output", dest="tests_output", default=tests_output, help="Output folder where files will be stored")
    parser.add_option("--select-dir-rule", dest="select_dir_rule", default=r'\d+_.*', help="RegExp for tests directory")
    parser.add_option("--select-ini-rule", dest="select_ini_rule", default=r'.*', help="RegExp for tests subdirs")
    parser.add_option("--select-artifact-rule", dest="select_artifact_rule", default=r'.*/profiler.*\.json$', help="RegExp for artifact files")

    parser.set_usage("""%prog [options]""")
    return parser


def parse_args(parser):
    """Parses argument using given parses and check resulting value combination"""
    options, args = parser.parse_args()
    return options, args,


def main():
    parser = create_parser()
    options, args = parse_args(parser)

    tester = FlowTester(**options.__dict__)
    tester.run()


if __name__ == '__main__':
    main()

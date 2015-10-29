#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs

import sys
import os


sys.path.append(os.getcwd())

from flowrunner.system import python
python.init()

from optparse import OptionParser
from flowrunner.testing import dynamic
from flowrunner.testing.dynamic import all_tests
from flowrunner.utils import strings
from flowrunner.utils import io


try:
    from psutil import cpu_count
except ImportError as e:
    from flowrunner.utils.simple_psutil import cpu_count
    print 'psutil lib missing, using simple_psutil cpu_count'


def create_parser():
    """Creates command line parse"""
    parser = OptionParser()

    parser.add_option("-i", "--include", dest="includes", metavar="TESTNAME", default=[], action="append",
                      help="Turn on specific perf, by default all perf are included")
    parser.add_option("-x", "--exclude", dest="excludes", metavar="TESTNAME", default=[], action="append",
                      help="Turn off specific perf")
    parser.add_option("-c", "--core", dest="cores", metavar="CORE", default=[], action="append",
                      help="Try test with this amount of core, by default 1...N, where N is maximum cores available")

    parser.add_option("-o", "--output", dest="output", default='performance.json',
                      help="Output location")
    parser.add_option("-d", "--duration", dest="timeout", metavar="DURATION", default=0.4,
                      help="Maximum duration per one test case")
    parser.add_option("-t", "--tries", dest="tries", metavar="TRIES", default=2,
                      help="Number of tries for each test")
    parser.add_option("-q", "--quiet", dest="quiet", default=True, action="store_false",
                      help="Do not print any output")
    parser.add_option("-H", "--human", dest="human", default=False, action="store_true",
                      help="Output in human-readable format")

    parser.set_usage("""%prog [options]""")
    return parser


def parse_args(parser):
    global print_output, human_format

    """Parses argument using given parses and check resulting value combination"""
    options, args = parser.parse_args()

    includes = set(options.includes) if options.includes else set(all_tests.keys())
    if options.excludes:
        includes = includes - set(options.excludes)

    if not options.cores:
        options.cores = range(1, cpu_count(logical=True) + 1)
    else:
        options.cores = [int(value) for value in options.cores]

    if options.human:
        human_format = True

    options.tries = int(options.tries)
    options.timeout = float(options.timeout)
    print_output = options.quiet

    assert options.tries > 0, 'Number of tries must be positive integer'
    assert options.timeout > 0, 'Timeout value must be positive number'

    return options, args, includes


def main():
    parser = create_parser()
    options, args, includes = parse_args(parser)

    print includes

    performance = dynamic.run_benchmarks(
        tests=includes,
        timeout=options.timeout,
        tries=options.tries,
        cores=options.cores
    )

    info = dict()
    info['tests'] = performance

    io.mkdir(options.output)
    print strings.to_json(info, options.output)


if __name__ == '__main__':
    main()

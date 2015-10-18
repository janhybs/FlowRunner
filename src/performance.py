#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs

from optparse import OptionParser
from testing import static, dynamic
from testing.dynamic import all_tests
from utils import pluck, strings

try:
    from psutil import cpu_count
except ImportError as e:
    from utils.simple_psutil import cpu_count

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
    (options, args) = parser.parse_args()

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
    (options, args, includes) = parse_args(parser)

    print includes

    binary_info = static.get_binary_info()
    arch_info = static.get_arch_info()

    performance = dynamic.run_benchmarks(
        tests=includes,
        timeout=options.timeout,
        tries=options.tries,
        cores=options.cores
    )

    info = dict()
    info['arch'] = arch_info
    info['bins'] = binary_info
    info['tests'] = performance

    print strings.to_json(info, 'performance.json')





# python main.py -o NPROC:1 -o NPROC:2 -o "NPROC:3 4" -o NPROC:6:5:19 -o NPROC:100:105 -o "A:1 3 5 9" -o  "B:foo bar" "echo '{NPROC} {A} {A} {B}'"
# python main.py -o NPROC:1 -o NPROC:2 -o "NPROC:3 4" -o NPROC:6:5:19 -o NPROC:100:105 -o "A:1 3 5 9" -o  "B:foo bar" -o "S:2>&1 1>&2" "echo 'NP={NPROC} A={A} A={A} B={B}' {S}"
# python main.py -o NP:1 -o NP:2 -o "NP:3 4" -o "B:foo bar" "echo 'NP={NP} B={B}'"
# python main.py -o P:1:100 "echo [{P}%]"





if __name__ == '__main__':
    main()

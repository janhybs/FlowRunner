#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs
import copy

from optparse import OptionParser
from testing import static, dynamic
from utils import pluck, strings


def create_parser():
    """Creates command line parse"""
    parser = OptionParser()

    parser.add_option("-o", "--option", dest="variables", metavar="NAME:VALUE", default=[], action="append",
                      help="Add other possible value for given NAME")

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
    """Parses argument using given parses and check resulting value combination"""
    (options, args) = parser.parse_args()

    return options, args


def main():
    binary_info = static.get_binary_info()
    arch_info = static.get_arch_info()
    performance = dynamic.run_benchmarks(timeout=0.01)

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
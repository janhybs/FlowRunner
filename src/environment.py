#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs

from optparse import OptionParser
import sys
from testing import static, dynamic
from testing.dynamic import all_tests
from utils import pluck, strings

def create_parser():
    """Creates command line parse"""
    parser = OptionParser()

    parser.add_option("-o", "--output", dest="output", default='architecture.json',
                      help="Output location")

    parser.set_usage("""%prog [options]""")
    return parser


def parse_args(parser):
    """Parses argument using given parses and check resulting value combination"""
    (options, args) = parser.parse_args()
    return options, args


def inject(o, prop, value):
    path = prop.split('.')
    name = path[-1]
    del path[-1]

    root = o
    for piece in path:
        if piece in root:
            root = root[piece]
        else:
            root[piece] = dict()
            root = root[piece]
    root[name] = value


def main():
    parser = create_parser()
    options, args, = parse_args(parser)

    binary_info = static.get_binary_info()
    arch_info = static.get_arch_info()

    info = dict()
    info['arch'] = arch_info
    info['bins'] = binary_info

    for arg in args:
        path, value = str(arg).split('=', 2)
        inject(info, path, value)

    print strings.to_json(info, options.output)





# python main.py -o NPROC:1 -o NPROC:2 -o "NPROC:3 4" -o NPROC:6:5:19 -o NPROC:100:105 -o "A:1 3 5 9" -o  "B:foo bar" "echo '{NPROC} {A} {A} {B}'"
# python main.py -o NPROC:1 -o NPROC:2 -o "NPROC:3 4" -o NPROC:6:5:19 -o NPROC:100:105 -o "A:1 3 5 9" -o  "B:foo bar" -o "S:2>&1 1>&2" "echo 'NP={NPROC} A={A} A={A} B={B}' {S}"
# python main.py -o NP:1 -o NP:2 -o "NP:3 4" -o "B:foo bar" "echo 'NP={NP} B={B}'"
# python main.py -o P:1:100 "echo [{P}%]"





if __name__ == '__main__':
    main()

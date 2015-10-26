#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs

import sys, os
sys.path.append(os.getcwd())

from system import python
python.init()

from optparse import OptionParser
from testing import static
from utils import strings
from utils import io


def create_parser():
    """Creates command line parse"""
    parser = OptionParser()

    parser.add_option("-o", "--output", dest="output", default='architecture.json', help="Output location")

    parser.set_usage("""%prog [options] [NAME=VALUE]""")
    return parser


def parse_args(parser):
    """Parses argument using given parses and check resulting value combination"""
    options, args = parser.parse_args()
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

    io.mkdir(options.output)
    print strings.to_json(info, options.output)


if __name__ == '__main__':
    main()

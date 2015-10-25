#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs

import sys, os
sys.path.append(os.getcwd())

import json
from pbs.pbsscript import PBSScript
from optparse import OptionParser


def create_parser():
    """Creates command line parse"""
    parser = OptionParser()

    parser.add_option("-c", "--config", dest="config", default='config.json', help="Config location")
    parser.add_option("-o", "--output", dest="output", default='pbs.sh', help="Output location")
    parser.add_option("-i", "--interactive", dest="interactive", default=False, action="store_false", help="Output location")

    parser.set_usage("""%prog [options]""")
    return parser


def parse_args(parser):
    """Parses argument using given parses and check resulting value combination"""
    options, args = parser.parse_args()
    return options, args,


def main():
    parser = create_parser()
    options, args = parse_args(parser)
    root = os.path.abspath(os.path.dirname(options.config))

    with open(options.config, 'r') as fp:
        json_data = json.load(fp)

    script = PBSScript()
    script.header(json_data["pbs"])

    if options.interactive:
        print script.peek()
    else:
        for f in json_data["scripts"]:
            script.add_file(os.path.join(root, f))

        script.save(options.output)


if __name__ == '__main__':
    main()

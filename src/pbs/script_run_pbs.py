#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs

import sys, os
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), 'libs'))
sys.path.append(os.path.join(os.getcwd(), 'lib'))

import json
from pbs.pbsscript import PBSScript
from optparse import OptionParser


def create_parser():
    """Creates command line parse"""
    parser = OptionParser()

    parser.add_option("-s", "--script", dest="script", default='pbs.sh', help="Output location")
    parser.add_option("-p", "--period", dest="period", default="30", help="qstat period")

    parser.set_usage("""%prog [options]""")
    return parser


def parse_args(parser):
    """Parses argument using given parses and check resulting value combination"""
    options, args = parser.parse_args()
    options.period = max(int(options.period), 65)
    return options, args,


def main():
    parser = create_parser()
    options, args = parse_args(parser)

    script = PBSScript(options.script)
    script.start_job()
    script.wait_for_exit(options.period)


if __name__ == '__main__':
    main()

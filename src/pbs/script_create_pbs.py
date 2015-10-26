#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs

import sys, os
from utils.parser import Parser

sys.path.append(os.getcwd())

from system import python
python.init()

import json
from pbs.pbsscript import PBSScript


def create_parser():
    """Creates command line parse"""
    p = Parser()

    p.add("c config", dest="config", default='config.json', help="Config location")
    p.add("o output", dest="output", default='pbs.sh', help="Output location")
    p.add("i interactive", dest="interactive", default=False, action="store_false", help="Output location")

    p.set_usage("""%prog [options]""")
    return p


def main():
    options, args = create_parser().parse()
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

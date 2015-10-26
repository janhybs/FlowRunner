#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs

from optparse import OptionParser
import __builtin__
from runner.execution.utils.exec_util import expand_vars


class Parser(object):
    def __init__(self):
        self.options = {}
        self.parser = OptionParser()
        self.check_args = lambda options, args: (options, args)

    def add(self, flag_format, dest, default=None, action=None, help=None, expand=False, type=None, **kwargs):
        """
        Adds another option to parser
        :param flag_format: str short_format long_format (seperated by space)
        :param dest: str destination
        :param default: default value
        :param action: parser store action (store, store_true, store_false, append)
        :param help: help message
        :param expand: bool True/False for smart expanding
        :param type: str of desired final type (even at list) from package __builtin__
        :param kwargs: additional kwargs passed to optparser
        :return:
        """
        flags = str(flag_format).strip().split()
        flags = sorted(flags, lambda a, b: len(a) - len(b))
        if len(flags) == 1:
            flags[0] = '--' + flags[0] if len(flags[0]) > 1 else '-' + flags[0]
        else:
            flags[0], flags[1] = '-' + flags[0],  '--' + flags[1]

        kwargs['dest'] = dest
        kwargs['default'] = default
        kwargs['action'] = action if not expand else 'append'
        kwargs['help'] = help
        kwargs['type'] = type if not expand else None
        self.parser.add_option(*flags, **kwargs)

        kwargs['expand'] = expand
        kwargs['type'] = type
        self.options[dest] = kwargs

    def parse(self, args=None, values=None):
        """
        parse_args(args : [string] = sys.argv[1:],
                   values : Values = None)
        -> (values : Values, args : [string])

        Parse the command-line options found in 'args' (default:
        sys.argv[1:]).  Any errors result in a call to 'error()', which
        by default prints the usage message to stderr and calls
        sys.exit() with an error message.  On success returns a pair
        (values, args) where 'values' is an Values instance (with all
        your option values) and 'args' is the list of arguments left
        over after parsing options.
        """
        options, args = self.parser.parse_args(args, values)
        options, args = self.check_args(options, args)

        for name, value in self.options.items():
            if value['expand']:
                new_values = expand_vars(["{name}:{v}".format(name=name, v=v) for v in getattr(options, name)])
                new_values = new_values[name] if name in new_values else getattr(options, name)
                if value['type']:
                    convert = getattr(__builtin__, value['type'])
                    new_values = [convert(x) for x in new_values]

                setattr(options, name, new_values)

        options, args = self.check_args(options, args)
        return options, args

    def set_usage(self, usage):
        self.parser.set_usage(usage)
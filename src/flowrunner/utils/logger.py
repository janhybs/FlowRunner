#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs

import logging
import traceback
import datetime
import os

from flowrunner.utils import io

logging.basicConfig(
    filename=io.join_path(os.getcwd(), 'python.log'),
    level=logging.NOTSET,
    format='%(asctime)s %(name)s %(levelname)-4s: %(message)s'
)


class Logger(object):
    def __init__(self, name=__name__, debug=True):
        self.logger = logging.getLogger(name)
        self.level = 0

        # add console log
        if __debug__ or debug:
            stream = logging.StreamHandler()
            stream.setLevel(logging.NOTSET)
            self.logger.addHandler(stream)

        with open('python.log', 'a+') as fp:
            fp.write('-' * 110)
            fp.write('\n')
        self.info("{:%d-%m-%Y %H:%M:%S}".format(datetime.datetime.now()))

    def _log_traceback(self, method):
        tb = [line.strip() for line in traceback.format_stack()]
        method('Traceback:\n' + '\n'.join(tb))

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)
        self._log_traceback(self.logger.error)

    def exception(self, msg, exception, *args, **kwargs):
        self.logger.exception(msg, exc_info=exception, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(self._indent() + str(msg), *args, **kwargs)
        return self

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def _indent(self):
        return '' if self.level == 0 else '  ' * self.level + '- '

    def open(self):
        self.level += 1

    def close(self):
        self.level -= 1

    def __enter__(self):
        """
        Enter the runtime context related to this object.
        :return:
        """
        self.open()
        return self

    def __exit__(self, exception_type, exception_value, tb):
        """
        Exit the runtime context related to this object.
        :param exception_type:
        :param exception_value:
        :param tb:
        :return:
        """
        # add debug info
        if exception_type:
            print exception_type, exception_value, tb
            traceback.print_exception(exception_type, exception_value, tb)
            traceback.print_stack()
            self.exception('Exception in __exit__', exception_value)
            raise exception_value

        self.close()
        return self

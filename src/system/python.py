#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs

import os, sys
from utils.logger import Logger

logger = Logger(__name__)
required_version = (2, 7, 0)


def version():
    return '.'.join([str(x) for x in sys.version_info[0:3]])


def init(debug=True):
    """
    Function will test current python version and will update some path
    :return:
    """

    if debug:
        logger.debug('Running python {version}, {info}'.format(version=version(), info=sys.version_info))

    if sys.version_info < required_version:
        logger.error(
            'Python version is too low {version} please use higher version, recommended version is {rec}'.format(
                version=version(), rec=required_version))
        sys.exit(1)

    if debug:
        logger.debug('Updating sys.path...')
    sys.path.append(os.path.join(os.getcwd(), '..', 'libs'))
    sys.path.append(os.path.join(os.getcwd(), '..', 'lib'))

    if debug:
        logger.debug('Current sys.path:\n{paths}'.format(paths='\n'.join(sys.path)))

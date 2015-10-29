#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs
from flowrunner.utils import pluck


class PluckDict(list):
    def __init__(self, items):
        super(PluckDict, self).__init__(items)

    def __getattr__(self, item):
        return pluck.pluck(self, item)

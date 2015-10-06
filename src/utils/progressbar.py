#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs


import sys


class ProgressBar(object):
    # ▅▆▇░▓□■▒█▣○◉●◯
    def __init__(self, width=40, maximum=100, finished_char='.', waiting_char=' ', prefix='', suffix=''):
        self.width = width
        self.maximum = maximum
        self.finished_char = finished_char
        self.waiting_char = waiting_char
        self.prefix = prefix
        self.suffix = suffix
        self.last_progress = 0

    def progress(self, value=None):
        self.last_progress = value
        percent = float(value if value is not None else self.maximum) / self.maximum

        finished = int(percent * self.width)
        waiting = self.width - finished

        if self.prefix:
            sys.stdout.write(self.prefix.format(self=self))

        sys.stdout.write((finished * self.finished_char) + (waiting * self.waiting_char))

        if self.suffix:
            sys.stdout.write(self.suffix.format(self=self))

        sys.stdout.write('\r')
        sys.stdout.flush()


    def end(self):
        self.progress(self.maximum)
        sys.stdout.write('\n\r')
        sys.stdout.flush()
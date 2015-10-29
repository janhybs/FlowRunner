#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs

from flowrunner.testing.perf.abstract import AbstractProcess


class MatrixCreate(AbstractProcess):
    """
    Test determining MEMORY performance
    Test complexity is constant
    """

    def test(self, result):
        import numpy

        rnd = numpy.random.RandomState(1234)
        i = 0
        score = 0
        while not self.exit.is_set():
            rnd.random_sample((100, 100))
            score = i
            i += 1
        result.value = score


class MatrixCreate2(AbstractProcess):
    """
    Test determining MEMORY performance
    Test complexity is not constant
    """

    def test(self, result):
        import numpy

        rnd = numpy.random.RandomState(1234)
        i = 0
        score = 0
        while not self.exit.is_set():
            rnd.random_sample((i + 1, i + 1))
            score = i
            i += 1
        result.value = score
#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs

from testing.perf.abstract import AbstractProcess


class Factorial(AbstractProcess):
    """
    Test determining CPU performance
    Test complexity constant
    """

    def test(self, result):
        import math

        i = 0
        n = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
        score = 0
        while not self.exit.is_set():
            math.factorial(n[i % 10])
            score = i
            i += 1
        result.value = score

    def factorial(self, n):
        # return math.factorial(n)
        return reduce(lambda x, y: x * y, [1] + range(1, n + 1))


class Factorial2(AbstractProcess):
    """
    Test determining CPU performance
    Test complexity is not constant (possible n)
    """

    def test(self, result):
        import math

        i = 0
        score = 0
        while not self.exit.is_set():
            math.factorial(i)
            score += i
            i += 1
        result.value = score

    def factorial(self, n):
        # return math.factorial(n)
        return reduce(lambda x, y: x * y, [1] + range(1, n + 1))
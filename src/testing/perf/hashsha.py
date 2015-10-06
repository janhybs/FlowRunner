#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs

import hashlib

from testing.perf.abstract import AbstractProcess


class HashSHA(AbstractProcess):
    """
    Test determining CPU performance
    Test complexity is constant
    """

    def test(self, result):
        i = 0
        score = 0
        while not self.exit.is_set():
            hashlib.sha512('1234').hexdigest()
            score = i
            i += 1
        result.value = score


class HashSHA2(AbstractProcess):
    """
    Test determining CPU and MEMORY performance
    Test complexity is not constant
    """

    def test(self, result):
        i = 0
        score = 0
        while not self.exit.is_set():
            hashlib.sha512(i * 'a').hexdigest()
            score += i
            i += 1
        result.value = score
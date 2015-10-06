#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs

from copy import copy as shallowcopy
from copy import deepcopy as deepcopy
from testing.clockrate import BenchmarkMeasurement


# tests
from testing.perf.factorial import Factorial, Factorial2
from testing.perf.forloop import ForLoop, ForLoop2
from testing.perf.hashsha import HashSHA, HashSHA2
from testing.perf.matrixcreate import MatrixCreate, MatrixCreate2
from testing.perf.matrixsolve import MatrixSolve, MatrixSolve2
from testing.perf.stringconcat import StringConcat, StringConcat2

try:
    from psutil import cpu_count
except ImportError as e:
    from utils.simple_psutil import cpu_count

    print 'psutil lib missing, using simple_psutil cpu_count'

try:
    from psutil import virtual_memory
except ImportError as e:
    from utils.simple_psutil import virtual_memory

    print 'psutil lib missing, using simple_psutil virtual_memory'

all_tests = {
    # constant complexity
    'for-loop': ForLoop,
    'factorial': Factorial,
    'hash-sha': HashSHA,
    'matrix-creation': MatrixCreate,
    'matrix-solve': MatrixSolve,
    'string-concat': StringConcat,

    # increasing complexity
    '_for-loop': ForLoop2,
    '_factorial': Factorial2,
    '_hash-sha': HashSHA2,
    '_matrix-creation': MatrixCreate2,
    '_matrix-solve': MatrixSolve2,
    '_string-concat': StringConcat2
}


def run_benchmarks(tests=None, cores=None, timeout=0.4, tries=2):
    tests = shallowcopy(all_tests.keys()) if tests is None else set(tests)
    cores = range(1, cpu_count(logical=True) + 1) if cores is None else cores

    measurement = BenchmarkMeasurement()
    measurement.configure(timeout, tries, cores)

    info = dict()
    for test in all_tests:
        if test not in tests:
            continue

        try:
            info[test] = measurement.measure(all_tests.get(test), test)
        except Exception as e:
            print e

    return info
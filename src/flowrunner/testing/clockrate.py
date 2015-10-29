# encoding: utf-8
# author:   Jan Hybs

import time

from flowrunner.utils.strings import human_readable


try:
    from pluck import pluck
except ImportError as e:
    from flowrunner.utils import pluck

    print 'pluck lib missing, using local copy'

from flowrunner.utils.timer import Timer
from flowrunner.utils.progressbar import ProgressBar


timer = Timer()


class BenchmarkMeasurement(object):
    def __init__(self):
        self.timeout = .5
        self.tries = 3
        self.processes = 1
        self.print_output = True
        self.human_format = False

    def measure(self, cls, name, timeout=None, tries=None, processes=None):
        timeout = timeout if timeout is not None else self.timeout
        tries = tries if tries is not None else self.tries
        processes = processes if processes is not None else self.processes

        pb = ProgressBar(maximum=tries, width=30, prefix="{self.name:35}",
                         suffix=" {self.last_progress}/{self.maximum}")

        measure_result = list()
        for no_cpu in processes:
            pb.name = "{:s} {:d} {:s}".format(name, no_cpu, 'core' if no_cpu == 1 else 'cores')
            results = list()
            for i in range(0, tries):
                if self.print_output:
                    pb.progress(i)

                targets = [cls() for j in range(0, no_cpu)]

                with timer.measured("{:s} {:d}".format(name, i), False):
                    # start processes
                    for target in targets:
                        target.start()

                    # wait for timeout
                    time.sleep(timeout)

                    # send exit status
                    for target in targets:
                        target.shutdown()

                    # join threads
                    for target in targets:
                        target.join()

                tmp = dict()
                tmp['duration'] = timer.time()
                tmp['value'] = sum(pluck(targets, 'result.value'))
                tmp['exit'] = not max(pluck(targets, 'terminated'))
                results.append(tmp)

            if self.print_output:
                pb.end()

            result = dict()
            result['processes'] = no_cpu
            # result['exit'] = min(pluck(results, 'exit'))
            result['duration'] = sum(pluck(results, 'duration')) / float(tries)
            result['value'] = sum(pluck(results, 'value')) / float(tries)
            result['performance'] = result['value'] / result['duration']
            result['effectiveness'] = (result['value'] / result['duration']) / no_cpu

            if self.human_format:
                result['value'] = human_readable(result['value'])
                result['performance'] = human_readable(result['performance'])
                result['effectiveness'] = human_readable(result['effectiveness'])

            measure_result.append(result)

        return measure_result

    def configure(self, timeout, tries, processes):
        self.timeout = timeout
        self.tries = tries
        self.processes = processes if type(processes) is list else [processes]
# encoding: utf-8
# author:   Jan Hybs

import Queue
import subprocess
import threading


class AsyncReader(threading.Thread):
    """
    Helper class to implement asynchronous reading of a file
    in a separate thread. Pushes read lines on a queue to
    be consumed in another thread.
    """

    def __init__(self, fd, queue):
        assert isinstance(queue, Queue.Queue)
        assert callable(fd.readline)
        threading.Thread.__init__(self)
        self._fd = fd
        self._queue = queue

    def run(self):
        """The body of the tread: read lines and put them on the queue."""
        for line in iter(self._fd.readline, ''):
            self._queue.put(line.rstrip('\n'))

    def eof(self):
        """Check whether there is no more content to expect."""
        return not self.is_alive() and self._queue.empty()


class AsyncProcess(object):
    """
    Helper class which executed shell command and via two AsyncReader (for error and output) will offer results outputs
    """

    def __init__(self, command, shell=True):
        self.command = command
        self.shell = shell
        self.process = None
        self.exit_code = None

        self.stdout_queue = None
        self.stderr_queue = None

        self.stdout_reader = None
        self.stderr_reader = None

    def run(self):
        """
        run process
        :return: tuple of stdout_queue and stderr_queue Queue
        """
        self.process = subprocess.Popen(self.command, shell=self.shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # prepare queues and returns it

        self.stdout_queue = Queue.Queue()
        self.stdout_reader = AsyncReader(self.process.stdout, self.stdout_queue)
        self.stdout_reader.start()

        self.stderr_queue = Queue.Queue()
        self.stderr_reader = AsyncReader(self.process.stderr, self.stderr_queue)
        self.stderr_reader.start()

        return self.stdout_queue, self.stderr_queue

    def wait(self):
        """
        join thread and waits until everything is done
        :return:
        """
        # check process existence
        if not self.process:
            raise

        # Let's be tidy and join the threads we've started.
        self.process.wait()
        self.stdout_reader.join()
        self.stderr_reader.join()
        self.exit_code = self.process.returncode

        return self.exit_code

    def is_running(self):
        """
        :return: True if process has not ended yet
        """
        return not self.stdout_reader.eof() or not self.stderr_reader.eof()

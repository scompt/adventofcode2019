#!/usr/bin/env python

import sys  # isort:skip

sys.path.insert(0, "..")  # isort:skip
from intcode import IntcodeComputer  # isort:skip

import queue
import threading
from functools import lru_cache
from itertools import count


def computer_generator(program):
    while True:
        oq = queue.Queue(1)
        iq = queue.Queue(2)
        computer = IntcodeComputer(program[:], iq, oq, threading.Condition())

        def process(x, y):
            iq.put(x)
            iq.put(y)
            computer.run()
            return oq.get()

        yield process


def range_overlap(range1, range2):
    """
    >>> len(range_overlap((1,5), (3,7)))
    3
    >>> len(range_overlap((2,3), (5,6)))
    0
    """
    return range(max(range1[0], range2[0]), min(range1[1], range2[1]))


@lru_cache(maxsize=1024)
def beam(y):
    if y < 3:
        return (0, 0)

    started = 0
    for x in count(beam(y - 1)[0]):
        seen = False
        computer = next(computers)
        detected = computer(x, y)

        if not started and detected:
            started = x

        if started and not detected:
            return (started, x)


def seek_in_beam(size):
    for y in count(size - 1):
        this_row = beam(y)
        if this_row[1] - this_row[0] < size:
            continue

        prev_row = beam(y - (size - 1))
        if len(range_overlap(this_row, prev_row)) >= size:
            return (this_row[0], y - size + 1)


if __name__ == "__main__":
    lines = sys.stdin.readlines()
    program = IntcodeComputer.read_input(lines[0])
    computers = computer_generator(program)

    for i in range(3, 101):
        x, y = seek_in_beam(i)
        print(i, x, y, x * 10_000 + y, beam.cache_info())

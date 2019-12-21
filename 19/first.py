#!/usr/bin/env python

import sys  # isort:skip

sys.path.insert(0, "..")  # isort:skip
from intcode import IntcodeComputer  # isort:skip

import queue
import threading


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


if __name__ == "__main__":
    lines = sys.stdin.readlines()
    program = IntcodeComputer.read_input(lines[0])
    computers = computer_generator(program)

    points = 0
    for y in range(50):
        for x in range(50):
            computer = next(computers)
            points += computer(x, y)

    print(points)

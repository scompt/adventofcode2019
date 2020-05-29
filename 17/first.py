#!/usr/bin/env python

import sys  # isort:skip

sys.path.insert(0, "..")  # isort:skip
from intcode import IntcodeComputer  # isort:skip

import queue
import threading
from textwrap import dedent


def alignment_parameter_sum(camera):
    """
    >>> inp = r'''
    ... ..#..........
    ... ..#..........
    ... #######...###
    ... #.#...#...#.#
    ... #############
    ... ..#...#...#..
    ... ..#####...^..
    ... '''
    >>> alignment_parameter_sum(dedent(inp).strip().split('\\n'))
    76
    """
    intersections = find_intersections(camera)
    return sum(i[0] * i[1] for i in intersections)


def find_intersections(camera):
    """
    >>> inp = r'''
    ... ..#..........
    ... ..#..........
    ... #######...###
    ... #.#...#...#.#
    ... #############
    ... ..#...#...#..
    ... ..#####...^..
    ... '''
    >>> find_intersections(dedent(inp).strip().split('\\n'))
    [(2, 2), (2, 4), (6, 4), (10, 4)]
    """
    locs = {}
    for y in range(len(camera)):
        for x in range(len(camera[0])):
            locs[(x, y)] = camera[y][x]

    intersections = []
    for yy in range(1, y):
        for xx in range(1, x):
            if (
                locs[(xx, yy)] == "#"
                and locs[(xx + 1, yy)] == "#"
                and locs[(xx - 1, yy)] == "#"
                and locs[(xx, yy + 1)] == "#"
                and locs[(xx, yy - 1)] == "#"
            ):
                intersections.append((xx, yy))
    return intersections


class ASCII:
    def __init__(self, input_queue):
        self.input_queue = input_queue
        self.camera = ""

    def run(self):
        self.camera = ""
        while True:
            self.camera += chr(self.input_queue.get())
            if self.camera[-2:] == "\n\n":
                break


if __name__ == "__main__":
    lines = sys.stdin.readlines()
    program = IntcodeComputer.read_input(lines[0])
    program[0] = 2

    oq = queue.Queue(1)
    iq = queue.Queue(1)
    ready = threading.Condition()

    ascii = ASCII(oq)
    computer = IntcodeComputer(program[:], iq, oq, ready)

    ascii_thread = threading.Thread(target=ascii.run, name="ASCII")
    computer_thread = threading.Thread(target=computer.run, name="Computer")

    ascii_thread.start()
    computer_thread.start()

    ascii_thread.join()
    computer_thread.join()

    print(alignment_parameter_sum(ascii.camera[:-2].split("\n")))

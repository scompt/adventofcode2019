#!/usr/bin/env python

import sys
sys.path.insert(0, "..")
from intcode import IntcodeComputer

from itertools import groupby


if __name__ == "__main__":
    import sys

    lines = sys.stdin.readlines()
    program = IntcodeComputer.read_input(lines[0])
    computer = IntcodeComputer(program)
    computer.run()

    out = computer.flush_output()
    gb = groupby(enumerate(out), lambda x: x[0] // 3)
    ys = [y for y in (list(x[1]) for x in gb)]
    insts = [(y[0][1], y[1][1], y[2][1]) for y in ys]

    blocks = set()
    for x, y, id in insts:
        if id == 2:
            blocks.add((x, y))

    print(len(blocks))

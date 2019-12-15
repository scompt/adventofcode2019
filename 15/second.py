#!/usr/bin/env python

import sys  # isort:skip

sys.path.insert(0, "..")  # isort:skip
from intcode import IntcodeComputer  # isort:skip

import queue
import threading
from collections import defaultdict
from enum import IntEnum
from functools import partial
from operator import itemgetter


class Direction(IntEnum):
    START = 0
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4


class Tile(IntEnum):
    UNKNOWN = -1
    WALL = 0
    OPEN = 1
    OXYGEN = 2


def neighbors(loc):
    yield (Direction.NORTH, (loc[0], loc[1] - 1))
    yield (Direction.SOUTH, (loc[0], loc[1] + 1))
    yield (Direction.WEST, (loc[0] + 1, loc[1]))
    yield (Direction.EAST, (loc[0] - 1, loc[1]))


class Droid:
    def __init__(self, input_queue, output_queue, output_ready, path, area):
        self.area = defaultdict(lambda: Tile.UNKNOWN)
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.output_ready = output_ready
        self.path = path
        self.area = area
        self.last_tile = Tile.OPEN

    def output(self, val):
        self.output_queue.put(val)
        with self.output_ready:
            self.output_ready.notify_all()

    def run(self):
        for movement, location in self.path[1:]:
            self.output(movement)
            self.last_tile = Tile(self.input_queue.get())
            self.area[location] = self.last_tile
        self.output(99)


def run_it(program, path, area):
    oq = queue.Queue(1)
    iq = queue.Queue(1)
    ready = threading.Condition()

    droid = Droid(oq, iq, ready, path, area)
    computer = IntcodeComputer(program[:], iq, oq, ready)

    droid_thread = threading.Thread(target=droid.run, name="Droid")
    computer_thread = threading.Thread(target=computer.run, name="Computer")

    droid_thread.start()
    computer_thread.start()

    droid_thread.join()
    computer_thread.join()

    return droid.last_tile


def show_area(area, droid_loc=None):
    min_x = min(area.keys(), key=itemgetter(0))[0]
    min_y = min(area.keys(), key=itemgetter(1))[1]
    max_x = max(area.keys(), key=itemgetter(0))[0]
    max_y = max(area.keys(), key=itemgetter(1))[1]

    out = ""
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            loc = (x, y)
            if loc == (0, 0):
                out += "X"
            elif loc == droid_loc:
                out += "D"
            elif area[loc] == Tile.UNKNOWN:
                out += " "
            elif area[loc] == Tile.WALL:
                out += "#"
            elif area[loc] == Tile.OPEN:
                out += "."
            elif area[loc] == Tile.OXYGEN:
                out += "O"
        out += "\n"
    out += "\n"
    print(out)


def max_distance(edges, start, area):

    complete = defaultdict(lambda: [])
    for k in list(edges.keys()):
        for v in list(edges[k]):
            complete[v].append(k)
            complete[k].append(v)

    distances = defaultdict(lambda: 10 ** 5)
    S = [start]
    distances[start] = 0

    while len(S) > 0:
        show_area(area)
        loc = S.pop(0)

        for node in complete[loc]:
            area[node] = Tile.OXYGEN
            if distances[loc] + 1 < distances[node]:
                distances[node] = distances[loc] + 1
                S.insert(0, node)
    return max(distances.values())


def discover_area(program):
    area = defaultdict(lambda: Tile.UNKNOWN)
    area[(0, 0)] = Tile.OPEN
    edges = defaultdict(lambda: [])
    paths = []
    Q = [[(0, (0, 0))]]
    oxygen_loc = None

    while len(Q) > 0:
        path = Q.pop(0)
        show_area(area, path[-1][1])

        last_tile = run_it(program, path, area)

        if last_tile is Tile.OXYGEN:
            oxygen_loc = path[-1][1]

        if last_tile is Tile.WALL:
            continue

        if len(path) > 1:
            from_loc = path[-2][1]
            to_loc = path[-1][1]
            edges[from_loc].append(to_loc)

        last_step = path[-1]
        for neighbor in neighbors(last_step[1]):
            if area[neighbor[1]] is not Tile.UNKNOWN:
                continue
            newpath = path[:] + [neighbor]
            Q.append(newpath)

    return edges, oxygen_loc, area


if __name__ == "__main__":
    import sys

    lines = sys.stdin.readlines()
    program = IntcodeComputer.read_input(lines[0])
    edges, oxygen_loc, area = discover_area(program)
    print(max_distance(edges, oxygen_loc, area))

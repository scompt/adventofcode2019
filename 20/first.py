#!/usr/bin/env python

import operator
from collections import defaultdict
from textwrap import dedent


def dfs(edges, start, target):
    parents = {}
    discovered = set()
    Q = [start]

    while len(Q) > 0:
        node = Q.pop(0)
        if node in discovered:
            continue
        if node == target:
            p = []
            while node != start:
                p.insert(0, node)
                node = parents[node]
            return p

        discovered.add(node)

        for edge in edges[node]:
            if edge in discovered:
                continue

            parents[edge] = node
            Q.insert(0, edge)


def read_input(lines):
    """
    >>> inp = r'''
    ...          A
    ...          A
    ...   #######.#########
    ...   #######.........#
    ...   #######.#######.#
    ...   #######.#######.#
    ...   #######.#######.#
    ...   #####  B    ###.#
    ... BC...##  C    ###.#
    ...   ##.##       ###.#
    ...   ##...DE  F  ###.#
    ...   #####    G  ###.#
    ...   #########.#####.#
    ... DE..#######...###.#
    ...   #.#########.###.#
    ... FG..#########.....#
    ...   ###########.#####
    ...              Z
    ...              Z
    ... '''
    >>> r = read_input(dedent(inp)[1:].rstrip().split('\\n'))
    """
    chars = defaultdict(lambda: " ")
    max_x = max_y = 0
    for y, line in enumerate(lines):
        max_y = max(y, max_y)
        for x, char in enumerate(line):
            max_x = max(x, max_x)
            chars[(x, y)] = char
    width = max_x - 3
    height = max_y - 3

    edges = defaultdict(lambda: [])
    portals = defaultdict(lambda: [])
    for y in range(max_y):
        for x in range(max_x):
            loc = (x, y)
            char = chars[loc]
            if char != ".":
                continue

            for n in neighbors(loc):
                n_loc = tuple(map(operator.add, loc, n))

                if chars[n_loc] == ".":
                    edges[loc].append(n_loc)
                elif chars[n_loc].isalpha():
                    nn_loc = tuple(map(operator.add, n_loc, n))
                    portal_label = "".join(sorted([chars[n_loc], chars[nn_loc]]))
                    portals[portal_label].append(loc)

    start = portals.pop("AA")[0]
    end = portals.pop("ZZ")[0]

    for portal_from, portal_to in portals.values():
        edges[portal_from].append(portal_to)
        edges[portal_to].append(portal_from)

    return edges, start, end


def neighbors(loc):
    yield ((+1, 0))
    yield ((-1, 0))
    yield ((0, +1))
    yield ((0, -1))


if __name__ == "__main__":
    import sys

    lines = sys.stdin.readlines()
    edges, start, end = read_input(l.rstrip() for l in lines)
    print(len(dfs(edges, start, end)))

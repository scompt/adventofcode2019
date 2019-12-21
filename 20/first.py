#!/usr/bin/env python

import operator
from collections import defaultdict
from textwrap import dedent


def ignore_portals_neighbors(edges, portals, node):
    e = (node[0], node[1])
    for n in edges[e]:
        yield (n[0], n[1], 0)


def first_portals_neighbors(edges, portals, node):
    e = (node[0], node[1])
    for n in edges[e]:
        yield (n[0], n[1], 0)

    for outer, inner in portals:
        if e == inner:
            yield (outer[0], outer[1], 0)
        elif e == outer:
            yield (inner[0], inner[1], 0)


def second_portals_neighbors(edges, portals, node):
    e = (node[0], node[1])
    for n in edges[e]:
        yield (n[0], n[1], node[2])

    z = node[2]
    for outer, inner in portals:
        if e == outer and z > 0:
            yield (inner[0], inner[1], z - 1)
        elif e == inner and z < 200:
            yield (outer[0], outer[1], z + 1)


node_neighbors = first_portals_neighbors


def dfs(edges, portals, start, target):
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

        for edge in node_neighbors(edges, portals, node):
            if edge in discovered:
                continue

            parents[edge] = node
            Q.append(edge)


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
    >>> edges, portals, start, end = read_input(dedent(inp)[1:].rstrip().split('\\n'))
    >>> start
    (9, 2, 0)
    >>> end
    (13, 16, 0)
    >>> portals
    dict_values([((2, 8), (9, 6)), ((2, 13), (6, 10)), ((2, 15), (11, 12))])
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
    portals = defaultdict(lambda: (None, None))
    for y in range(max_y):
        for x in range(max_x):
            loc = (x, y)
            char = chars[loc]
            if char != ".":
                continue

            for n in loc_neighbors(loc):
                n_loc = tuple(map(operator.add, loc, n))

                if chars[n_loc] == ".":
                    edges[loc].append(n_loc)
                elif chars[n_loc].isalpha():
                    nn_loc = tuple(map(operator.add, n_loc, n))
                    portal_label = "".join(sorted([chars[n_loc], chars[nn_loc]]))

                    if x == 2 or y == 2 or x == max_x - 2 or y == max_y - 2:
                        portals[portal_label] = (loc, portals[portal_label][1])
                    else:
                        portals[portal_label] = (portals[portal_label][0], loc)

    start = portals.pop("AA")[0]
    end = portals.pop("ZZ")[0]

    start = (start[0], start[1], 0)
    end = (end[0], end[1], 0)

    return edges, portals.values(), start, end


def loc_neighbors(loc):
    yield ((+1, 0))
    yield ((-1, 0))
    yield ((0, +1))
    yield ((0, -1))


if __name__ == "__main__":
    import sys

    lines = sys.stdin.readlines()
    edges, portals, start, end = read_input(l.rstrip() for l in lines)
    print(len(dfs(edges, portals, start, end)))

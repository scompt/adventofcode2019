#!/usr/bin/env python

from collections import defaultdict


def read_input(lines):
    """
    >>> inp = r'''
    ... COM)B
    ... B)C
    ... C)D
    ... D)E
    ... E)F
    ... B)G
    ... G)H
    ... D)I
    ... E)J
    ... J)K
    ... K)L
    ... '''
    >>> read_input(inp.strip().split('\\n'))
    """
    orbits = {}
    for l in lines:
        object1, object2 = l.strip().split(")")
        orbits[object2] = object1
    return orbits


def count_orbits(orbits):
    orbit_set = set()
    for source in orbits.keys():
        origin = source
        while source != "COM":
            target = orbits[source]
            orbit_set.add((origin, target))
            source = target
    return len(orbit_set)


if __name__ == "__main__":
    import sys

    inp = read_input(sys.stdin.readlines())
    orbit_count = count_orbits(inp)
    print(orbit_count)

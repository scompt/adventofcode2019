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
    >>> out = read_input(inp.strip().split('\\n'))
    >>> sorted(out.items())
    [('B', 'COM'), ('C', 'B'), ('D', 'C'), ('E', 'D'), ('F', 'E'), ('G', 'B'), ('H', 'G'), ('I', 'D'), ('J', 'E'), ('K', 'J'), ('L', 'K')]
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


def get_ancestors(orbits, obj):
    """
    >>> orbits = {'B': 'COM', 'C': 'B', 'D': 'C', 'E': 'D', 'F': 'E', 'G': 'B', 'H': 'G', 'I': 'D', 'J': 'E', 'K': 'J', 'L': 'K', 'YOU': 'K', 'SAN': 'I'}
    >>> get_ancestors(orbits, 'D')
    ['C', 'B', 'COM']
    """
    ancestors = []
    while obj != "COM":
        obj = orbits[obj]
        ancestors.append(obj)
    return ancestors


def find_common_ancestor(orbits, object1="YOU", object2="SAN"):
    """
    >>> orbits = {'B': 'COM', 'C': 'B', 'D': 'C', 'E': 'D', 'F': 'E', 'G': 'B', 'H': 'G', 'I': 'D', 'J': 'E', 'K': 'J', 'L': 'K', 'YOU': 'K', 'SAN': 'I'}
    >>> find_common_ancestor(orbits)
    'D'
    """
    ancestors1 = get_ancestors(orbits, object1)
    ancestors2 = get_ancestors(orbits, object2)

    last = None
    for i in range(-1, -max(len(ancestors1), len(ancestors2)), -1):
        if ancestors1[i] == ancestors2[i]:
            last = ancestors1[i]
        else:
            return last
    raise Exception("No common ancstor")


def distance_between(orbits, source, target):
    """
    >>> orbits = {'B': 'COM', 'C': 'B', 'D': 'C', 'E': 'D', 'F': 'E', 'G': 'B', 'H': 'G', 'I': 'D', 'J': 'E', 'K': 'J', 'L': 'K', 'YOU': 'K', 'SAN': 'I'}
    >>> distance_between(orbits, 'YOU', 'D')
    4
    """
    distance = 0
    while source != target:
        distance += 1
        source = orbits[source]
    return distance


def minimum_orbital_transfers(orbits):
    """
    >>> orbits = {'B': 'COM', 'C': 'B', 'D': 'C', 'E': 'D', 'F': 'E', 'G': 'B', 'H': 'G', 'I': 'D', 'J': 'E', 'K': 'J', 'L': 'K', 'YOU': 'K', 'SAN': 'I'}
    >>> minimum_orbital_transfers(orbits)
    4
    """
    common = find_common_ancestor(orbits, "YOU", "SAN")
    distance1 = distance_between(orbits, orbits["YOU"], common)
    distance2 = distance_between(orbits, orbits["SAN"], common)
    return distance1 + distance2


if __name__ == "__main__":
    import sys

    inp = read_input(sys.stdin.readlines())
    print(minimum_orbital_transfers(inp))

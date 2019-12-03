#!/usr/bin/env python

import sys
from operator import add


def parse(inp):
    """
    >>> list(parse('R8,U5,L5,D3'))
    [('R', 8), ('U', 5), ('L', 5), ('D', 3)]
    >>> list(parse('U7,R6,D4,L4'))
    [('U', 7), ('R', 6), ('D', 4), ('L', 4)]
    >>> list(parse('R75,D30,R83,U83,L12,D49,R71,U7,' + \
                   'L72,U62,R66,U55,R34,D71,R55,D58,R83'))
    [('R', 75), ('D', 30), ('R', 83), ('U', 83), ('L', 12), ('D', 49), ('R', 71), ('U', 7), ('L', 72), ('U', 62), ('R', 66), ('U', 55), ('R', 34), ('D', 71), ('R', 55), ('D', 58), ('R', 83)]
    >>> list(parse('R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51,U98,R91,D20,R16,D67,R40,U7,R15,U6,R7'))
    [('R', 98), ('U', 47), ('R', 26), ('D', 63), ('R', 33), ('U', 87), ('L', 62), ('D', 20), ('R', 33), ('U', 53), ('R', 51), ('U', 98), ('R', 91), ('D', 20), ('R', 16), ('D', 67), ('R', 40), ('U', 7), ('R', 15), ('U', 6), ('R', 7)]
    """
    return ((turn[0], int(turn[1:])) for turn in inp.split(','))


def generate_path(parsed):
    """
    >>> generate_path(parse('R8,U5,L5,D3'))
    [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (7, 5), (6, 5), (5, 5), (4, 5), (3, 5), (3, 4), (3, 3), (3, 2)]
    >>> generate_path(parse('U7,R6,D4,L4'))
    [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (6, 6), (6, 5), (6, 4), (6, 3), (5, 3), (4, 3), (3, 3), (2, 3)]
    """
    current_location = (0, 0)
    path = [current_location]

    for direction, distance in parsed:
        if direction == 'D':
            operand = (0, -1)
        elif direction == 'U':
            operand = (0, 1)
        elif direction == 'L':
            operand = (-1, 0)
        elif direction == 'R':
            operand = (1, 0)

        for _ in range(distance):
            current_location = tuple(map(add, current_location, operand))
            path.append(current_location)
    return path


def intersections(path1, path2):
    """
    >>> path1 = generate_path(parse('R8,U5,L5,D3'))
    >>> path2 = generate_path(parse('U7,R6,D4,L4'))
    >>> intersections(path1, path2)
    [(3, 3), (6, 5)]
    """
    path1 = set(path1)
    path2 = set(path2)
    candidates = list(path1.intersection(path2))
    candidates.remove((0, 0))
    return candidates


def simplest_path(path1, path2):
    """
    >>> path1 = generate_path(parse('R8,U5,L5,D3'))
    >>> path2 = generate_path(parse('U7,R6,D4,L4'))
    >>> simplest_path(path1, path2)
    30
    """
    candidates = intersections(path1, path2)
    candidates.sort(key=lambda r: path1.index(r) + path2.index(r))
    return path1.index(candidates[0]) + path2.index(candidates[0])


def nearest_intersection_distance(path1, path2):
    """
    >>> path1 = generate_path(parse('R8,U5,L5,D3'))
    >>> path2 = generate_path(parse('U7,R6,D4,L4'))
    >>> nearest_intersection_distance(path1, path2)
    6
    """
    candidates = intersections(path1, path2)
    candidates.sort(key=lambda r: abs(r[0]) + abs(r[1]))
    return abs(candidates[0][0]) + abs(candidates[0][1])


if __name__ == "__main__":
    import sys
    lines = sys.stdin.readlines()
    path1 = generate_path(parse(lines[0]))
    path2 = generate_path(parse(lines[1]))
    print(simplest_path(path1, path2))

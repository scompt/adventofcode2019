#!/usr/bin/env python

import operator
from math import atan2, pi, sqrt
from textwrap import dedent


def read_input(lines):
    """
    >>> inp = r'''
    ... .#..#
    ... .....
    ... #####
    ... ....#
    ... ...##
    ... '''
    >>> read_input(dedent(inp).strip())
    {(4, 4), (1, 2), (4, 0), (3, 4), (4, 3), (4, 2), (0, 2), (2, 2), (1, 0), (3, 2)}
    """
    asteroids = set()
    for y, line in enumerate(lines.split("\n")):
        for x in range(len(line.strip())):
            if line[x] == "#":
                asteroids.add((x, y))
    return asteroids


def is_asteroid_between_stacked(from_asteroid, to_asteroid, asteroids):
    """
    >>> inp = r'''
    ... .#..#
    ... .....
    ... #####
    ... ....#
    ... ...##
    ... '''
    >>> asteroids = read_input(dedent(inp).strip())
    >>> is_asteroid_between_stacked((4, 0), (4, 2), asteroids)
    False
    >>> is_asteroid_between_stacked((4, 0), (4, 3), asteroids)
    True
    >>> is_asteroid_between_stacked((3, 4), (3, 2), asteroids)
    False
    """
    if from_asteroid[0] != to_asteroid[0]:
        raise Exception("Not stacked")
    lower, upper = sorted([from_asteroid[1], to_asteroid[1]])
    for intermediate_asteroid in asteroids:
        if (
            intermediate_asteroid == from_asteroid
            or intermediate_asteroid == to_asteroid
        ):
            # Skip the from and to asteroids
            continue

        if intermediate_asteroid[0] != from_asteroid[0]:
            # Intermediate not stacked
            continue

        if lower <= intermediate_asteroid[1] <= upper:
            # intermediate_asteroid is in the way
            return True

    return False


def almost_equal(left, right, decimal=6):
    # https://docs.scipy.org/doc/numpy/reference/generated/numpy.testing.assert_array_almost_equal.html
    return abs(left - right) < 1.5 * 10 ** (-decimal)


def is_asteroid_between_nonstacked(from_asteroid, to_asteroid, asteroids):
    """
    >>> asteroids = {(4, 0), (1, 2), (3, 4), (4, 3), (4, 2), (0, 2), (2, 2), (1, 0), (3, 2)}
    >>> # is_asteroid_between_nonstacked((0, 2), (1, 2), asteroids)
    False
    >>> is_asteroid_between_nonstacked((0, 2), (2, 2), asteroids)
    True
    >>> is_asteroid_between_nonstacked((1, 0), (3, 4), asteroids)
    True
    >>> is_asteroid_between_nonstacked((1, 0), (4, 2), asteroids)
    False

    >>> inp = r'''
    ... ......#.#.
    ... #..#.#....
    ... ..#######.
    ... .#.#.###..
    ... .#..#.....
    ... ..#....#.#
    ... #..#....#.
    ... .##.#..###
    ... ##...#..#.
    ... .#....####
    ... '''
    >>> asteroids = read_input(dedent(inp).strip())
    >>> is_asteroid_between_nonstacked((0, 8), (8, 0), asteroids)
    True
    """
    if from_asteroid[0] == to_asteroid[0]:
        raise Exception("Stacked")

    # y = mx+b
    m = (to_asteroid[1] - from_asteroid[1]) / (to_asteroid[0] - from_asteroid[0])
    b = (
        from_asteroid[1]
        - (to_asteroid[1] - from_asteroid[1])
        / (to_asteroid[0] - from_asteroid[0])
        * from_asteroid[0]
    )
    for intermediate_asteroid in asteroids:
        if (
            intermediate_asteroid == from_asteroid
            or intermediate_asteroid == to_asteroid
        ):
            # Skip the from and to asteroids
            continue

        if not almost_equal(intermediate_asteroid[1], m * intermediate_asteroid[0] + b):
            # intermediate asteroid is not on the same line as from and to
            continue
        else:
            pass

        if (
            (
                from_asteroid[0] <= intermediate_asteroid[0] <= to_asteroid[0]
                and from_asteroid[1] <= intermediate_asteroid[1] <= to_asteroid[1]
            )
            or (
                from_asteroid[0] <= intermediate_asteroid[0] <= to_asteroid[0]
                and from_asteroid[1] >= intermediate_asteroid[1] >= to_asteroid[1]
            )
            or (
                from_asteroid[0] >= intermediate_asteroid[0] >= to_asteroid[0]
                and from_asteroid[1] <= intermediate_asteroid[1] <= to_asteroid[1]
            )
            or (
                from_asteroid[0] >= intermediate_asteroid[0] >= to_asteroid[0]
                and from_asteroid[1] >= intermediate_asteroid[1] >= to_asteroid[1]
            )
        ):
            return True

    return False


def best_asteroid(asteroids):
    """
    >>> inp = r'''
    ... .#..#
    ... .....
    ... #####
    ... ....#
    ... ...##
    ... '''
    >>> asteroids = read_input(dedent(inp).strip())
    >>> best_asteroid(asteroids)
    ((3, 4), 8)
    
    >>> inp = r'''
    ... ......#.#.
    ... #..#.#....
    ... ..#######.
    ... .#.#.###..
    ... .#..#.....
    ... ..#....#.#
    ... #..#....#.
    ... .##.#..###
    ... ##...#..#.
    ... .#....####
    ... '''
    >>> asteroids = read_input(dedent(inp).strip())
    >>> best_asteroid(asteroids)
    ((5, 8), 33)
    
    >>> inp = r'''
    ... #.#...#.#.
    ... .###....#.
    ... .#....#...
    ... ##.#.#.#.#
    ... ....#.#.#.
    ... .##..###.#
    ... ..#...##..
    ... ..##....##
    ... ......#...
    ... .####.###.
    ... '''
    >>> asteroids = read_input(dedent(inp).strip())
    >>> best_asteroid(asteroids)
    ((1, 2), 35)
    
    >>> inp = r'''
    ... .#..#..###
    ... ####.###.#
    ... ....###.#.
    ... ..###.##.#
    ... ##.##.#.#.
    ... ....###..#
    ... ..#.#..#.#
    ... #..#.#.###
    ... .##...##.#
    ... .....#.#..
    ... '''
    >>> asteroids = read_input(dedent(inp).strip())
    >>> best_asteroid(asteroids)
    ((6, 3), 41)
    
    >>> inp = r'''
    ... .#..##.###...#######
    ... ##.############..##.
    ... .#.######.########.#
    ... .###.#######.####.#.
    ... #####.##.#.##.###.##
    ... ..#####..#.#########
    ... ####################
    ... #.####....###.#.#.##
    ... ##.#################
    ... #####.##.###..####..
    ... ..######..##.#######
    ... ####.##.####...##..#
    ... .#####..#.######.###
    ... ##...#.##########...
    ... #.##########.#######
    ... .####.#.###.###.#.##
    ... ....##.##.###..#####
    ... .#.#.###########.###
    ... #.#.#.#####.####.###
    ... ###.##.####.##.#..##
    ... '''
    >>> asteroids = read_input(dedent(inp).strip())
    >>> best_asteroid(asteroids)
    ((11, 13), 210)
    """
    candidates = dict(
        [(asteroid, detect_asteroids(asteroid, asteroids)) for asteroid in asteroids]
    )
    lens = list(((k, len(v)) for k, v in candidates.items()))
    best_asteroid, detected_count = max(lens, key=operator.itemgetter(1))
    return best_asteroid, detected_count


def detect_asteroids(from_asteroid, asteroids):
    """
    >>> inp = r'''
    ... .#..#
    ... .....
    ... #####
    ... ....#
    ... ...##
    ... '''
    >>> asteroids = read_input(dedent(inp).strip())
    >>> detect_asteroids((1, 0), asteroids)
    {(4, 4), (4, 0), (1, 2), (4, 2), (0, 2), (2, 2), (3, 2)}
    >>> detect_asteroids((4, 2), asteroids)
    {(4, 0), (3, 4), (4, 3), (1, 0), (3, 2)}
    """
    detected = set()
    for to_asteroid in asteroids:
        if from_asteroid == to_asteroid:
            # Skip the same asteroid
            continue

        if to_asteroid[0] == from_asteroid[0]:
            # The two asteroids are stacked on top of each other
            if not is_asteroid_between_stacked(from_asteroid, to_asteroid, asteroids):
                detected.add(to_asteroid)

        else:
            if not is_asteroid_between_nonstacked(
                from_asteroid, to_asteroid, asteroids
            ):
                detected.add(to_asteroid)

    return detected


def laser(asteroids, location):
    """
    >>> inp = r'''
    ... .#....#####...#..
    ... ##...##.#####..##
    ... ##...#...#.#####.
    ... ..#.....X...###..
    ... ..#.#.....#....##
    ... '''
    >>> asteroids = read_input(dedent(inp).strip())
    >>> monitoring_location = (8, 3)
    >>> list(laser(asteroids, monitoring_location))
    [(8, 1), (9, 0), (9, 1), (10, 0), (9, 2), (11, 1), (12, 1), (11, 2), (15, 1), (12, 2), (13, 2), (14, 2), (15, 2), (12, 3), (16, 4), (15, 4), (10, 4), (4, 4), (2, 4), (2, 3), (0, 2), (1, 2), (0, 1), (1, 1), (5, 2), (1, 0), (5, 1), (6, 1), (6, 0), (7, 0), (8, 0), (10, 1), (14, 0), (16, 1), (13, 3), (14, 3)]
    
    >>> inp = r'''
    ... .#..##.###...#######
    ... ##.############..##.
    ... .#.######.########.#
    ... .###.#######.####.#.
    ... #####.##.#.##.###.##
    ... ..#####..#.#########
    ... ####################
    ... #.####....###.#.#.##
    ... ##.#################
    ... #####.##.###..####..
    ... ..######..##.#######
    ... ####.##.####...##..#
    ... .#####..#.######.###
    ... ##...#.##########...
    ... #.##########.#######
    ... .####.#.###.###.#.##
    ... ....##.##.###..#####
    ... .#.#.###########.###
    ... #.#.#.#####.####.###
    ... ###.##.####.##.#..##
    ... '''
    >>> asteroids = read_input(dedent(inp).strip())
    >>> monitoring_location = (11, 13)
    >>> destroyed_asteroids = list(laser(asteroids, monitoring_location))
    >>> destroyed_asteroids[0:3]
    [(11, 12), (12, 1), (12, 2)]
    >>> destroyed_asteroids[9]
    (12, 8)
    >>> destroyed_asteroids[19]
    (16, 0)
    >>> destroyed_asteroids[49]
    (16, 9)
    >>> destroyed_asteroids[99]
    (10, 16)
    >>> destroyed_asteroids[198]
    (9, 6)
    >>> destroyed_asteroids[199]
    (8, 2)
    >>> destroyed_asteroids[200]
    (10, 9)
    >>> destroyed_asteroids[298]
    (11, 1)
    
    """
    ordered = []
    for asteroid in asteroids:
        if location == asteroid:
            continue

        dist = sqrt(
            (location[1] - asteroid[1]) * (location[1] - asteroid[1])
            + (location[0] - asteroid[0]) * (location[0] - asteroid[0])
        )
        angle = atan2(asteroid[1] - location[1], asteroid[0] - location[0])
        ordered.append((asteroid, dist, (angle - (-pi / 2) + (2 * pi)) % (2 * pi)))

    sought_angle = -0.000001
    sought_distance = 0

    ordered = sorted(ordered, key=operator.itemgetter(2))
    while len(ordered) > 0:
        try:
            sought = min(
                [x for x in ordered if x[2] > sought_angle],
                key=operator.itemgetter(2, 1),
            )
            sought_angle = sought[2]
            sought_distance = sought[1]
            ordered.remove(sought)
            yield (sought[0])
        except ValueError:
            sought_angle = -0.000001


if __name__ == "__main__":
    import sys

    lines = sys.stdin.readlines()
    asteroids = read_input("".join(lines))
    monitoring_location, _ = best_asteroid(asteroids)
    lasered = list(laser(asteroids, monitoring_location))
    print(lasered[199][0] * 100 + lasered[199][1])

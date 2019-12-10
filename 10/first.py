#!/usr/bin/env python

import operator
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


if __name__ == "__main__":
    import sys

    lines = sys.stdin.readlines()
    asteroids = read_input("\n".join(lines))
    print(best_asteroid(asteroids)[1])

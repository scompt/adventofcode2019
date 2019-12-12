#!/usr/bin/env python


def fuel_for_mass(mass):
    """
    >>> fuel_for_mass(12)
    2
    >>> fuel_for_mass(14)
    2
    >>> fuel_for_mass(1969)
    654
    >>> fuel_for_mass(100756)
    33583
    >>> fuel_for_mass(0)
    0
    """
    return max(0, mass // 3 - 2)


def weigh_fuel(fuel):
    """
    >>> weigh_fuel(12)
    2
    >>> weigh_fuel(1969)
    966
    >>> weigh_fuel(100756)
    50346
    """
    fuel_mass = fuel_for_mass(fuel)
    if fuel_mass == 0:
        return 0
    else:
        return fuel_mass + weigh_fuel(fuel_mass)


if __name__ == "__main__":
    import sys

    print(sum(weigh_fuel(int(line.strip())) for line in sys.stdin.readlines()))

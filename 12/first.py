#!/usr/bin/env python

from collections import defaultdict
from itertools import combinations
from textwrap import dedent

from numpy import lcm


class Position(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, other):
        return (
            isinstance(other, Position)
            and self.x == other.x
            and self.y == other.y
            and self.z == other.z
        )

    def __repr__(self):
        return f"({self.x}, {self.y}, {self.z})"


class Velocity(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, other):
        return (
            isinstance(other, Velocity)
            and self.x == other.x
            and self.y == other.y
            and self.z == other.z
        )

    def __repr__(self):
        return f"({self.x}, {self.y}, {self.z})"


class Moon(object):
    def __init__(self, x, y, z):
        self.position = Position(int(x), int(y), int(z))
        self.velocity = Velocity(0, 0, 0)

    def energy(self):
        """
        >>> m = Moon(1, 2, -3)
        >>> m.energy()
        0
        >>> m.velocity.x = 1
        >>> m.energy()
        6
        """
        return sum(abs(getattr(self.position, axis)) for axis in ["x", "y", "z"]) * sum(
            abs(getattr(self.velocity, axis)) for axis in ["x", "y", "z"]
        )

    def __eq__(self, other):
        return (
            isinstance(self, Moon)
            and self.position == other.position
            and self.velocity == other.velocity
        )

    def __repr__(self):
        return f"<Moon position={self.position} velocity={self.velocity}>"


class System(object):
    def __init__(self, lines):
        """
        >>> inp = r'''
        ... <x=-1, y=0, z=2>
        ... <x=2, y=-10, z=-7>
        ... <x=4, y=-8, z=8>
        ... <x=3, y=5, z=-1>
        ... '''
        >>> System(inp.strip().split("\\n"))
        [<Moon position=(-1, 0, 2) velocity=(0, 0, 0)>, <Moon position=(2, -10, -7) velocity=(0, 0, 0)>, <Moon position=(4, -8, 8) velocity=(0, 0, 0)>, <Moon position=(3, 5, -1) velocity=(0, 0, 0)>]
        """
        self.moons = []
        for l in lines:
            coords = dict(c.split("=") for c in l[1:-1].split(", "))
            self.moons.append(Moon(**coords))

    def find_period(self, axis):
        target = [
            (getattr(m.position, axis), getattr(m.velocity, axis)) for m in self.moons
        ]
        step = 0
        while True:
            self.step()
            step += 1

            candidate = [
                (getattr(m.position, axis), getattr(m.velocity, axis))
                for m in self.moons
            ]
            if candidate == target:
                return step

    def step(self, count=1):
        """
        >>> inp = r'''
        ... <x=-1, y=0, z=2>
        ... <x=2, y=-10, z=-7>
        ... <x=4, y=-8, z=8>
        ... <x=3, y=5, z=-1>
        ... '''
        >>> s = System(inp.strip().split("\\n"))
        >>> s.step()
        >>> s
        [<Moon position=(2, -1, 1) velocity=(3, -1, -1)>, <Moon position=(3, -7, -4) velocity=(1, 3, 3)>, <Moon position=(1, -7, 5) velocity=(-3, 1, -3)>, <Moon position=(2, 2, 0) velocity=(-1, -3, 1)>]
        >>> s.step()
        >>> s
        [<Moon position=(5, -3, -1) velocity=(3, -2, -2)>, <Moon position=(1, -2, 2) velocity=(-2, 5, 6)>, <Moon position=(1, -4, -1) velocity=(0, 3, -6)>, <Moon position=(1, -4, 2) velocity=(-1, -6, 2)>]
        """
        for _ in range(count):
            self.apply_gravity()
            self.apply_velocity()

    def apply_gravity(self):
        """
        >>> inp = r'''
        ... <x=-1, y=0, z=2>
        ... <x=2, y=-10, z=-7>
        ... <x=4, y=-8, z=8>
        ... <x=3, y=5, z=-1>
        ... '''
        >>> s = System(inp.strip().split("\\n"))
        >>> s.apply_gravity()
        >>> s
        [<Moon position=(-1, 0, 2) velocity=(3, -1, -1)>, <Moon position=(2, -10, -7) velocity=(1, 3, 3)>, <Moon position=(4, -8, 8) velocity=(-3, 1, -3)>, <Moon position=(3, 5, -1) velocity=(-1, -3, 1)>]
        """
        for a, b in combinations(self.moons, 2):
            for axis in ["x", "y", "z"]:
                if getattr(a.position, axis) > getattr(b.position, axis):
                    a_diff = -1
                    b_diff = +1
                elif getattr(a.position, axis) < getattr(b.position, axis):
                    a_diff = +1
                    b_diff = -1
                else:
                    continue

                setattr(a.velocity, axis, getattr(a.velocity, axis) + a_diff)
                setattr(b.velocity, axis, getattr(b.velocity, axis) + b_diff)

    def apply_velocity(self):
        """
        >>> inp = r'''
        ... <x=-1, y=0, z=2>
        ... <x=2, y=-10, z=-7>
        ... <x=4, y=-8, z=8>
        ... <x=3, y=5, z=-1>
        ... '''
        >>> s = System(inp.strip().split("\\n"))
        >>> s.apply_gravity()
        >>> s.apply_velocity()
        >>> s
        [<Moon position=(2, -1, 1) velocity=(3, -1, -1)>, <Moon position=(3, -7, -4) velocity=(1, 3, 3)>, <Moon position=(1, -7, 5) velocity=(-3, 1, -3)>, <Moon position=(2, 2, 0) velocity=(-1, -3, 1)>]
        """
        for moon in self.moons:
            for axis in ["x", "y", "z"]:
                new_axis_position = getattr(moon.position, axis) + getattr(
                    moon.velocity, axis
                )
                setattr(moon.position, axis, new_axis_position)

    def energy(self):
        """
        >>> inp = r'''
        ... <x=-1, y=0, z=2>
        ... <x=2, y=-10, z=-7>
        ... <x=4, y=-8, z=8>
        ... <x=3, y=5, z=-1>
        ... '''
        >>> s = System(inp.strip().split("\\n"))
        >>> s.energy()
        0
        >>> s.step(10)
        >>> s.energy()
        179

        >>> inp = r'''
        ... <x=-8, y=-10, z=0>
        ... <x=5, y=5, z=10>
        ... <x=2, y=-7, z=3>
        ... <x=9, y=-8, z=-3>
        ... '''
        >>> s = System(inp.strip().split("\\n"))
        >>> s.energy()
        0
        >>> s.step(100)
        >>> s.energy()
        1940
        """
        return sum(moon.energy() for moon in self.moons)

    def __repr__(self):
        return str(self.moons)


if __name__ == "__main__":
    import sys

    periods = []
    lines = [l.strip() for l in sys.stdin.readlines()]
    for axis in ["x", "y", "z"]:
        s = System(lines)
        periods.append(s.find_period(axis))
    print(lcm.reduce(periods))

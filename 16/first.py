#!/usr/bin/env python

from itertools import cycle, islice, repeat

BASE_PATTERN = [0, 1, 0, -1]


def pattern(index):
    """
    >>> loop = pattern(0)
    >>> list(islice(loop, 0, 5))
    [1, 0, -1, 0, 1]

    >>> loop = pattern(1)
    >>> list(islice(loop, 0, 15))
    [0, 1, 1, 0, 0, -1, -1, 0, 0, 1, 1, 0, 0, -1, -1]

    >>> loop = pattern(2)
    >>> list(islice(loop, 0, 10))
    [0, 0, 1, 1, 1, 0, 0, 0, -1, -1]
    """

    def inner(index):
        for el in cycle(BASE_PATTERN):
            for r in repeat(el, index + 1):
                yield r

    b = inner(index)
    next(b)
    return b


def phase(input):
    """
    >>> input = '12345678'
    >>> output = phase(input)
    >>> output
    '48226158'
    >>> output = phase(output)
    >>> output
    '34040438'
    >>> output = phase(output)
    >>> output
    '03415518'
    >>> output = phase(output)
    >>> output
    '01029498'
    """
    output = []
    for index in range(len(input)):
        patt = pattern(index)
        output.append(str(sum(int(j) * next(patt) for j in input))[-1])
    return "".join(output)


def process(input, phase_count):
    """
    >>> process('80871224585914546619083218645595', 100)[0:8]
    '24176176'
    >>> process('19617804207202209144916044189917', 100)[0:8]
    '73745418'
    >>> process('69317163492948606335995924319873', 100)[0:8]
    '52432133'
    """
    for i in range(phase_count):
        input = phase(input)
    return input


if __name__ == "__main__":
    import sys

    line = sys.stdin.readlines()[0].strip()
    print(process(line, 100)[0:8])

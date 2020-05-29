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
            yield from repeat(el, index + 1)

    b = inner(index)
    next(b)
    return b


def phase(input, start=0):
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

    >>> phase('15518', 3)
    '29498'
    """
    output = []
    for index in range(len(input)):
        # print(index)
        # print(index+start)
        patt = list(islice(pattern(index+start), start, start+len(input)))
        print(patt)
        patt = iter(patt)
        output.append(str(abs(sum(int(j) * next(patt) for j in input)) % 10))
    return "".join(output)


def process(input, phase_count, start=0):
    """
    >>> process('80871224585914546619083218645595', 100)[0:8]
    '24176176'
    >>> process('19617804207202209144916044189917', 100)[0:8]
    '73745418'
    >>> process('69317163492948606335995924319873', 100)[0:8]
    '52432133'
    
    >>> process('45678', 4, 3)
    '29498'
    """
    for _ in range(phase_count):
        print(_)
        print(input)
        input = phase(input, start)
    return input


def woot(line):
    """
    >>> woot('03036732577212944063491565474664')
    '84462026'
    >>> woot('02935109699940807407585447034323')
    '78725270'
    >>> woot('03081770884921959731165446850517')
    '53553731'
    """
    message_offset = int(line[0:7])
    # print(message_offset)
    # print(list(islice(pattern(message_offset), message_offset, message_offset+8)))
    # print(list(islice(pattern(message_offset+1), message_offset+1, message_offset+8+1)))
    input = (line*10000)[message_offset:message_offset+8]
    return process(input, 100, message_offset)

if __name__ == "__main__":
    import sys

    line = sys.stdin.readlines()[0].strip()
    print(woot(line))

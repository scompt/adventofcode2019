#!/usr/bin/env python

from textwrap import dedent


def read_input(inp):
    """
    >>> read_input('1,2,3,4,5')
    [1, 2, 3, 4, 5]
    >>> inp = r'''
    ... 1,9,10,3,
    ... 2,3,11,0,
    ... 99,
    ... 30,40,50
    ... '''
    >>> read_input(dedent(inp).strip())
    [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]
    """
    return [int(i.strip()) for i in inp.split(',')]


def process(memory):
    """
    >>> process([1, 0, 0, 2, 99])
    [1, 0, 2, 2, 99]
    >>> process([1,9,10,3,2,3,11,0,99,30,40,50])
    [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]
    >>> process([1,0,0,0,99])
    [2, 0, 0, 0, 99]
    >>> process([2,3,0,3,99])
    [2, 3, 0, 6, 99]
    >>> process([2,4,4,5,99,0])
    [2, 4, 4, 5, 99, 9801]
    >>> process([1,1,1,4,99,5,6,0,99])
    [30, 1, 1, 4, 2, 5, 6, 0, 99]
    """
    pc = 0

    while True:
        intcode = memory[pc]

        if intcode == 1:
            operand1 = memory[memory[pc+1]]
            operand2 = memory[memory[pc+2]]
            result = operand1 + operand2
            memory[memory[pc+3]] = result
            pc += 4

        elif intcode == 2:
            operand1 = memory[memory[pc+1]]
            operand2 = memory[memory[pc+2]]
            result = operand1 * operand2
            memory[memory[pc+3]] = result
            pc += 4

        elif intcode == 99:
            return memory

        else:
            raise Exception("Unexpected intcode: %s" % intcode)


def search(memory, target):
    orig = memory

    for noun in range(0, 100):
        for verb in range(0, 100):
            memory = orig[:]
            memory[1] = noun
            memory[2] = verb
            out = process(memory)

            if out[0] == target:
                return (noun, verb)


if __name__ == "__main__":
    import sys
    memory = read_input(','.join(sys.stdin.readlines()))
    noun, verb = search(memory, 19690720)
    print(100 * noun + verb)

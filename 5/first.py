#!/usr/bin/env python

from textwrap import dedent


class HaltException(Exception):
    pass


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
    return [int(i.strip()) for i in inp.split(",")]


def read_memory(memory, val, immediate_mode):
    if immediate_mode:
        return val
    else:
        return memory[val]


def parse_modes(modes):
    return [bool(int(i)) for i in f"{modes:04d}"[::-1]]


def op_add(memory, modes, pc, inputs):
    operand1 = read_memory(memory, memory[pc + 1], modes[0])
    operand2 = read_memory(memory, memory[pc + 2], modes[1])
    result = operand1 + operand2
    memory[memory[pc + 3]] = result
    return 4


def op_mul(memory, modes, pc, inputs):
    operand1 = read_memory(memory, memory[pc + 1], modes[0])
    operand2 = read_memory(memory, memory[pc + 2], modes[1])
    result = operand1 * operand2
    memory[memory[pc + 3]] = result
    return 4


def op_load(memory, modes, pc, inputs):
    loc = memory[pc + 1]
    val = int(inputs.pop(0))
    memory[loc] = val
    return 2


def op_print(memory, modes, pc, inputs):
    loc = memory[pc + 1]
    print(memory[loc])
    return 2


def op_halt(memory, modes, pc, inputs):
    raise HaltException()


operations = {
    1: op_add,
    2: op_mul,
    3: op_load,
    4: op_print,
    99: op_halt,
}


def process(memory, inputs):
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

        try:
            opcode = intcode % 100
            modes = parse_modes(intcode // 100)
            op = operations[opcode]
            skip_len = op(memory, modes, pc, inputs)
            pc += skip_len

        except HaltException:
            return memory

        except KeyError:
            raise Exception("Unexpected intcode: %s" % intcode)


if __name__ == "__main__":
    import sys

    lines = sys.stdin.readlines()
    memory = read_input(lines[0])
    inputs = lines[1:]
    process(memory, inputs)

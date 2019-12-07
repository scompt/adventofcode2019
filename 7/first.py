#!/usr/bin/env python

import operator
from itertools import permutations
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


def op_add(memory, modes, pc, inputs, outputs):
    operand1 = read_memory(memory, memory[pc + 1], modes[0])
    operand2 = read_memory(memory, memory[pc + 2], modes[1])
    result = operand1 + operand2
    memory[memory[pc + 3]] = result
    return pc + 4


def op_mul(memory, modes, pc, inputs, outputs):
    operand1 = read_memory(memory, memory[pc + 1], modes[0])
    operand2 = read_memory(memory, memory[pc + 2], modes[1])
    result = operand1 * operand2
    memory[memory[pc + 3]] = result
    return pc + 4


def op_load(memory, modes, pc, inputs, outputs):
    loc = memory[pc + 1]
    val = int(inputs.pop(0))
    memory[loc] = val
    return pc + 2


def op_print(memory, modes, pc, inputs, outputs):
    loc = memory[pc + 1]
    outputs.append(memory[loc])
    return pc + 2


def op_jump_if_true(memory, modes, pc, inputs, outputs):
    operand1 = read_memory(memory, memory[pc + 1], modes[0])
    operand2 = read_memory(memory, memory[pc + 2], modes[1])
    if operand1 > 0:
        return operand2
    else:
        return pc + 3


def op_jump_if_false(memory, modes, pc, inputs, outputs):
    operand1 = read_memory(memory, memory[pc + 1], modes[0])
    operand2 = read_memory(memory, memory[pc + 2], modes[1])
    if operand1 == 0:
        return operand2
    else:
        return pc + 3


def op_less_than(memory, modes, pc, inputs, outputs):
    operand1 = read_memory(memory, memory[pc + 1], modes[0])
    operand2 = read_memory(memory, memory[pc + 2], modes[1])
    loc = memory[pc + 3]
    memory[loc] = 1 if operand1 < operand2 else 0
    return pc + 4


def op_equals(memory, modes, pc, inputs, outputs):
    operand1 = read_memory(memory, memory[pc + 1], modes[0])
    operand2 = read_memory(memory, memory[pc + 2], modes[1])
    loc = memory[pc + 3]
    memory[loc] = 1 if operand1 == operand2 else 0
    return pc + 4


def op_halt(memory, modes, pc, inputs, outputs):
    raise HaltException()


operations = {
    1: op_add,
    2: op_mul,
    3: op_load,
    4: op_print,
    5: op_jump_if_true,
    6: op_jump_if_false,
    7: op_less_than,
    8: op_equals,
    99: op_halt,
}


def process(memory, inputs=[]):
    """
    >>> process([1, 0, 0, 2, 99])
    ([1, 0, 2, 2, 99], [])
    >>> process([1,9,10,3,2,3,11,0,99,30,40,50])
    ([3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50], [])
    >>> process([1,0,0,0,99])
    ([2, 0, 0, 0, 99], [])
    >>> process([2,3,0,3,99])
    ([2, 3, 0, 6, 99], [])
    >>> process([2,4,4,5,99,0])
    ([2, 4, 4, 5, 99, 9801], [])
    >>> process([1,1,1,4,99,5,6,0,99])
    ([30, 1, 1, 4, 2, 5, 6, 0, 99], [])
    """
    memory = memory[:]
    pc = 0
    outputs = []

    while True:
        intcode = memory[pc]

        try:
            opcode = intcode % 100
            modes = parse_modes(intcode // 100)
            op = operations[opcode]
            pc = op(memory, modes, pc, inputs, outputs)

        except HaltException:
            return (memory, outputs)

        except KeyError:
            raise Exception("Unexpected intcode: %s" % intcode)


def calculate_thruster(program, phase_sequence):
    """
    >>> program = read_input('3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0')
    >>> phase_sequence = '43210'
    >>> calculate_thruster(program, phase_sequence)
    43210
    >>> program = read_input('3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0')
    >>> phase_sequence = '01234'
    >>> calculate_thruster(program, phase_sequence)
    54321
    >>> program = read_input('3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0')
    >>> phase_sequence = '10432'
    >>> calculate_thruster(program, phase_sequence)
    65210
    """
    input_signal = 0

    for amp in range(len(phase_sequence)):
        phase = int(phase_sequence[amp])
        _, outputs = process(program, [phase, input_signal])
        input_signal = outputs[0]

    return input_signal


def optimize_thruster(program):
    """
    >>> program = read_input('3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0')
    >>> optimize_thruster(program)
    43210
    >>> program = read_input('3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0')
    >>> optimize_thruster(program)
    54321
    >>> program = read_input('3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0')
    >>> optimize_thruster(program)
    65210
    """
    phases = list(permutations(range(5)))
    thrusts = list(map(lambda p: calculate_thruster(program, p), phases))
    max_index, max_thrust = max(enumerate(thrusts), key=operator.itemgetter(1))
    return max_thrust


if __name__ == "__main__":
    import sys

    lines = sys.stdin.readlines()
    memory = read_input(lines[0])
    max_thrust = optimize_thruster(memory)
    print(max_thrust)

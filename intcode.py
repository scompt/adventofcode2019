#!/usr/bin/env python

import operator
import queue
import threading
from collections import defaultdict
from enum import IntEnum
from itertools import permutations
from textwrap import dedent


class Mode(IntEnum):
    ABSOLUTE = 0
    IMMEDIATE = 1
    RELATIVE = 2


def parse_modes(modes):
    """
    >>> parse_modes(2100) # doctest: +ELLIPSIS
    defaultdict(..., {0: <Mode.ABSOLUTE: 0>, 1: <Mode.ABSOLUTE: 0>, 2: <Mode.IMMEDIATE: 1>, 3: <Mode.RELATIVE: 2>})
    >>> parse_modes(2) # doctest: +ELLIPSIS
    defaultdict(..., {0: <Mode.RELATIVE: 2>})
    """
    return defaultdict(
        lambda: Mode.ABSOLUTE, enumerate([Mode(int(i)) for i in str(modes)[::-1]])
    )


class HaltException(Exception):
    pass


class IntcodeComputer(object):
    def __init__(self, program, input_queue, output_queue, input_ready):
        self.memory = defaultdict(lambda: 0, enumerate(program))
        self.pc = 0
        self.relative_base = 0
        self.input_queue = input_queue
        self.input_ready = input_ready
        self.output_queue = output_queue

        self.operations = {
            1: self.op_add,
            2: self.op_mul,
            3: self.op_load,
            4: self.op_print,
            5: self.op_jump_if_true,
            6: self.op_jump_if_false,
            7: self.op_less_than,
            8: self.op_equals,
            9: self.op_set_relative_base,
            99: self.op_halt,
        }

    @classmethod
    def read_input(cls, inp):
        """
        >>> IntcodeComputer.read_input('1,2,3,4,5')
        [1, 2, 3, 4, 5]
        >>> inp = r'''
        ... 1,9,10,3,
        ... 2,3,11,0,
        ... 99,
        ... 30,40,50
        ... '''
        >>> IntcodeComputer.read_input(dedent(inp).strip())
        [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]
        """
        return [int(i.strip()) for i in inp.split(",")]

    def read_memory(self, val, mode):
        if mode is Mode.ABSOLUTE:
            return self.memory[val]

        elif mode is Mode.IMMEDIATE:
            return val

        elif mode is Mode.RELATIVE:
            return self.memory[self.relative_base + val]

        else:
            raise Exception(f"Unknown mode: {mode}")

    def write_memory(self, loc, mode, val):
        if mode is Mode.ABSOLUTE:
            self.memory[loc] = val

        elif mode is Mode.IMMEDIATE:
            raise Exception("Can't write to IMMEDIATE mode parameters.")

        elif mode is Mode.RELATIVE:
            self.memory[loc + self.relative_base] = val

        else:
            raise Exception(f"Unknown mode: {mode}")

    def dump_memory(self):
        max_location = max(self.memory.keys())
        return [self.memory[loc] for loc in range(max_location + 1)]

    def flush_output(self):
        result = []
        while not self.output_queue.empty():
            result.append(self.output_queue.get())

        return result

    def op_add(self, modes):
        operand1 = self.read_memory(self.memory[self.pc + 1], modes[0])
        operand2 = self.read_memory(self.memory[self.pc + 2], modes[1])
        result = operand1 + operand2
        self.write_memory(self.memory[self.pc + 3], modes[2], result)
        return self.pc + 4

    def op_mul(self, modes):
        operand1 = self.read_memory(self.memory[self.pc + 1], modes[0])
        operand2 = self.read_memory(self.memory[self.pc + 2], modes[1])
        result = operand1 * operand2
        self.write_memory(self.memory[self.pc + 3], modes[2], result)
        return self.pc + 4

    def op_load(self, modes):
        # print('1234'*100)
        val = None
        while val is None:
            with self.input_ready:
                # print('7890'*2)
                self.input_ready.notify_all()
                # print('jljklk'*2)
            val = int(self.input_queue.get())
            # print(f'read: {val}')
            # print(f'ooo{val}ooo')

        self.write_memory(self.memory[self.pc + 1], modes[0], val)
        return self.pc + 2

    def op_print(self, modes):
        val = self.read_memory(self.memory[self.pc + 1], modes[0])
        self.output_queue.put(val)
        return self.pc + 2

    def op_jump_if_true(self, modes):
        operand1 = self.read_memory(self.memory[self.pc + 1], modes[0])
        operand2 = self.read_memory(self.memory[self.pc + 2], modes[1])
        if operand1 > 0:
            return operand2
        else:
            return self.pc + 3

    def op_jump_if_false(self, modes):
        operand1 = self.read_memory(self.memory[self.pc + 1], modes[0])
        operand2 = self.read_memory(self.memory[self.pc + 2], modes[1])
        if operand1 == 0:
            return operand2
        else:
            return self.pc + 3

    def op_less_than(self, modes):
        operand1 = self.read_memory(self.memory[self.pc + 1], modes[0])
        operand2 = self.read_memory(self.memory[self.pc + 2], modes[1])
        loc = self.memory[self.pc + 3]
        result = 1 if operand1 < operand2 else 0
        self.write_memory(self.memory[self.pc + 3], modes[2], result)
        return self.pc + 4

    def op_equals(self, modes):
        operand1 = self.read_memory(self.memory[self.pc + 1], modes[0])
        operand2 = self.read_memory(self.memory[self.pc + 2], modes[1])
        loc = self.memory[self.pc + 3]
        result = 1 if operand1 == operand2 else 0
        self.write_memory(self.memory[self.pc + 3], modes[2], result)
        return self.pc + 4

    def op_set_relative_base(self, modes):
        operand1 = self.read_memory(self.memory[self.pc + 1], modes[0])
        self.relative_base += operand1
        return self.pc + 2

    def op_halt(self, modes):
        raise HaltException()

    def run(self):
        """
        >>> computer = IntcodeComputer([1, 0, 0, 2, 99])
        >>> computer.run()
        >>> computer.dump_memory()
        [1, 0, 2, 2, 99]
        >>> computer = IntcodeComputer([1,9,10,3,2,3,11,0,99,30,40,50])
        >>> computer.run()
        >>> computer.dump_memory()
        [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]
        >>> computer = IntcodeComputer([1,0,0,0,99])
        >>> computer.run()
        >>> computer.dump_memory()
        [2, 0, 0, 0, 99]
        >>> computer = IntcodeComputer([2,3,0,3,99])
        >>> computer.run()
        >>> computer.dump_memory()
        [2, 3, 0, 6, 99]
        >>> computer = IntcodeComputer([2,4,4,5,99,0])
        >>> computer.run()
        >>> computer.dump_memory()
        [2, 4, 4, 5, 99, 9801]
        >>> computer = IntcodeComputer([1,1,1,4,99,5,6,0,99])
        >>> computer.run()
        >>> computer.dump_memory()
        [30, 1, 1, 4, 2, 5, 6, 0, 99]

        >>> computer = IntcodeComputer([109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99])
        >>> computer.run()
        >>> computer.flush_output()
        [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
        >>> computer = IntcodeComputer([1102,34915192,34915192,7,4,7,99,0])
        >>> computer.run()
        >>> computer.flush_output()
        [1219070632396864]
        >>> computer = IntcodeComputer([104,1125899906842624,99])
        >>> computer.run()
        >>> computer.flush_output()
        [1125899906842624]
        """
        while True:
            intcode = self.memory[self.pc]
            # print(f'xxxx{intcode}')

            try:
                opcode = intcode % 100
                modes = parse_modes(intcode // 100)
                op = self.operations[opcode]
                self.pc = op(modes)

            except HaltException:
                # print("halting")
                return

            except KeyError:
                raise Exception("Unexpected intcode: %s" % intcode)

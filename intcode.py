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
    def __init__(self, program, input_queue=queue.Queue(), output_queue=queue.Queue()):
        self.memory = defaultdict(lambda: 0, enumerate(program))
        self.pc = 0
        self.relative_base = 0
        self.input_queue = input_queue
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
        val = int(self.input_queue.get())
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

            try:
                opcode = intcode % 100
                modes = parse_modes(intcode // 100)
                op = self.operations[opcode]
                self.pc = op(modes)

            except HaltException:
                return

            except KeyError:
                raise Exception("Unexpected intcode: %s" % intcode)


def calculate_thruster(program, phase_sequence):
    """
    >>> program = program = IntcodeComputer.read_input('3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0')
    >>> phase_sequence = '43210'
    >>> calculate_thruster(program, phase_sequence)
    43210
    >>> program = IntcodeComputer.read_input('3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0')
    >>> phase_sequence = '01234'
    >>> calculate_thruster(program, phase_sequence)
    54321
    >>> program = IntcodeComputer.read_input('3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0')
    >>> phase_sequence = '10432'
    >>> calculate_thruster(program, phase_sequence)
    65210

    >>> program = IntcodeComputer.read_input('3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5')
    >>> phase_sequence = '98765'
    >>> calculate_thruster(program, phase_sequence)
    139629729
    >>> program = IntcodeComputer.read_input('3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10')
    >>> phase_sequence = '97856'
    >>> calculate_thruster(program, phase_sequence)
    18216
    """
    amp_count = len(phase_sequence)

    queues = [queue.Queue() for i in range(amp_count)]
    computers = [
        IntcodeComputer(program, queues[i], queues[(i + 1) % amp_count])
        for i in range(amp_count)
    ]
    threads = [threading.Thread(target=computer.run) for computer in computers]

    for i in range(amp_count):
        phase = int(phase_sequence[i])
        queues[i].put(phase)

    queues[0].put(0)

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    return queues[0].get()


def optimize_thruster(program, with_feedback):
    """
    >>> program = IntcodeComputer.read_input('3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0')
    >>> optimize_thruster(program, False)
    43210
    >>> program = IntcodeComputer.read_input('3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0')
    >>> optimize_thruster(program, False)
    54321
    >>> program = IntcodeComputer.read_input('3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0')
    >>> optimize_thruster(program, False)
    65210

    >>> program = IntcodeComputer.read_input('3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5')
    >>> optimize_thruster(program, True)
    139629729
    >>> program = IntcodeComputer.read_input('3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10')
    >>> optimize_thruster(program, True)
    18216
    """
    if with_feedback:
        phases = list(permutations([5, 6, 7, 8, 9]))
    else:
        phases = list(permutations([0, 1, 2, 3, 4]))

    thrusts = list(map(lambda p: calculate_thruster(program, p), phases))
    max_index, max_thrust = max(enumerate(thrusts), key=operator.itemgetter(1))
    return max_thrust


class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def right(self):
        return Direction((self.value + 1) % len(Direction))

    def left(self):
        return Direction((self.value - 1) % len(Direction))


direction_movement = {
    Direction.UP: (0, 1),
    Direction.RIGHT: (1, 0),
    Direction.DOWN: (0, -1),
    Direction.LEFT: (-1, 0),
}


class PaintRobot(object):
    def __init__(self, input_queue, output_queue):
        self.colors = defaultdict(lambda: 0, {(0, 0): 1})
        self.current_location = (0, 0)
        self.direction = Direction.UP

        self.input_queue = input_queue
        self.output_queue = output_queue

    def run(self):
        while True:
            current_color = self.colors[self.current_location]
            self.output_queue.put(current_color)

            color_to_paint = self.input_queue.get()
            if color_to_paint is None:
                return  # Sentinel
            self.colors[self.current_location] = color_to_paint

            turn_direction = self.input_queue.get()
            if turn_direction == 0:
                self.direction = self.direction.left()
            elif turn_direction == 1:
                self.direction = self.direction.right()

            increment = direction_movement[self.direction]
            self.current_location = (
                self.current_location[0] + increment[0],
                self.current_location[1] + increment[1],
            )

    def print_painted(self):
        min_x = min(self.colors, key=operator.itemgetter(0))[0]
        max_x = max(self.colors, key=operator.itemgetter(0))[0]
        min_y = max(self.colors, key=operator.itemgetter(1))[1]
        max_y = min(self.colors, key=operator.itemgetter(1))[1]

        for y in range(min_y, max_y - 1, -1):
            for x in range(min_x, max_x + 1):
                if self.colors[(x, y)] == 0:
                    print("#", end="")
                else:
                    print(".", end="")
            print()


if __name__ == "__main__":
    import sys

    lines = sys.stdin.readlines()
    memory = IntcodeComputer.read_input(lines[0])

    input_queue = queue.Queue()
    output_queue = queue.Queue()

    paint_robot = PaintRobot(output_queue, input_queue)
    robot_thread = threading.Thread(target=paint_robot.run)
    robot_thread.start()

    computer = IntcodeComputer(memory, input_queue, output_queue)
    computer_thread = threading.Thread(target=computer.run)
    computer_thread.start()

    computer_thread.join()
    output_queue.put(None)  # Sentinel
    paint_robot.print_painted()

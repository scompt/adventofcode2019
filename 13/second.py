#!/usr/bin/env python

import sys  # isort:skip

sys.path.insert(0, "..")  # isort:skip
from intcode import IntcodeComputer  # isort:skip

import os
import queue
import threading
from collections import defaultdict
from enum import IntEnum
from itertools import groupby
from operator import itemgetter
from time import sleep


def iterable_queue(q):
    return iter(lambda: q.get(), None)


class Tile(IntEnum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    PADDLE = 3
    BALL = 4


OBSTACLES = (Tile.WALL, Tile.BLOCK, Tile.PADDLE)


class Blah:
    def __init__(self, arcade, output_ready, output_queue):
        self.arcade = arcade
        self.output_ready = output_ready
        self.output_queue = output_queue

    def run(self):
        while True:
            # print('zxcv'*100)
            with self.output_ready:
                # print('qwer'*100)
                if self.output_ready.wait():
                    # print('asdf'*2)
                    tilt = self.arcade.paddle_tilt
                    self.output_queue.put(tilt)


class Arcade:
    def __init__(self, input_queue, output_queue, output_ready):
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.output_ready = output_ready

        self.direction = 0
        self.score = 0
        self.paddle = None
        self.previous_paddle = None
        self.paddle_tilt = 0
        self.ball = None
        self.previous_ball = None
        self.predicted_ball = None
        self.cleared = None
        self.skip_prediction = False
        self.seen_direction = False
        self.tiles = defaultdict(lambda: Tile.EMPTY)

    def __repr__(self):
        height = 22
        width = 37

        out = " " + "".join(str(i)[-1] for i in range(width)) + "\n"
        for y in range(height):
            out += str(y)[-1]
            for x in range(width):
                tile = self.tiles[(x, y)]

                if (x, y) == self.cleared:
                    out += "_"
                elif tile is Tile.WALL:
                    if (x, y) == self.predicted_ball:
                        out += "%"
                    else:
                        out += "█"
                elif tile is Tile.BLOCK:
                    if (x, y) == self.predicted_ball:
                        out += "*"
                    else:
                        out += "X"
                elif tile is Tile.PADDLE or (x, y) == self.paddle:
                    out += "="
                elif tile is Tile.BALL or (x, y) == self.ball:
                    if self.ball == self.predicted_ball:
                        out += "ø"
                    else:
                        out += "o"
                elif (x, y) == self.previous_ball and (x, y) == self.predicted_ball:
                    out += "◉"
                elif (x, y) == self.previous_ball:
                    out += "."
                elif (x, y) == self.predicted_ball:
                    out += "O"
                elif (x, y) == self.previous_paddle:
                    out += "-"
                else:
                    out += " "

            out += str(y)[-1]
            out += "\n"
        out += " " + "".join(str(i)[-1] for i in range(width)) + "\n"

        score_str = f" score: {self.score} "
        if len(score_str) % 2 == 0:
            score_str += " "

        if self.paddle_tilt == -1:
            paddle_str = " \\ "
        elif self.paddle_tilt == 1:
            paddle_str = " / "
        else:
            paddle_str = " | "

        width += 2
        out += "." * width
        out += "\n"
        out += "." * ((width - len(score_str)) // 2)
        out += score_str
        out += "." * ((width - len(score_str)) // 2)
        out += "\n"
        out += "." * ((width - len(paddle_str)) // 2)
        out += paddle_str
        out += "." * ((width - len(paddle_str)) // 2)
        out += "\n"
        out += "." * width
        out += "\n"

        return out

    def run(self):
        iq = iterable_queue(self.input_queue)
        gb = groupby(enumerate(iq), lambda x: x[0] // 3)
        ys = (y for y in (list(x[1]) for x in gb))
        insts = ((y[0][1], y[1][1], y[2][1]) for y in ys)

        for x, y, id in insts:
            # print(x,y,id)
            self.process(x, y, id)
            # if self.score and not any(t for t in self.tiles.values() if t == Tile.BLOCK):
            #     print(f'Score: {self.score}')
            #     return

    def make_prediction(self):
        if self.tiles[self.ball] != Tile.BALL:
            return

        ball = self.ball
        prev = self.previous_ball
        pred = self.predicted_ball

        direction = (ball[0] - prev[0], ball[1] - prev[1])
        while True:
            # print(f'prev:{prev} ball:{ball} pred:{pred} dir:{direction} ', end='')

            if (
                self.tiles[(ball[0] + direction[0], ball[1])] in OBSTACLES
                and self.tiles[(ball[0], ball[1] + direction[1])] in OBSTACLES
            ):
                # print('1')
                direction = (-direction[0], -direction[1])
                pred = (ball[0] + direction[0], ball[1] + direction[1])

            elif self.tiles[(ball[0] + direction[0], ball[1])] in OBSTACLES:
                # print('2')
                # Direct x bounce, reverses x direction
                direction = (-direction[0], direction[1])
                pred = (ball[0] + direction[0], ball[1] + direction[1])

            elif self.tiles[(ball[0], ball[1] + direction[1])] in OBSTACLES:
                # print('3')
                # Direct y bounce in travel direction, reverses y direction
                direction = (direction[0], -direction[1])
                pred = (ball[0] + direction[0], ball[1] + direction[1])

            elif (
                self.tiles[(ball[0] + direction[0], ball[1] + direction[1])]
                in OBSTACLES
            ):
                # print('4')
                # Schräg y bounce in travel direction, reverses y direction
                direction = (-direction[0], -direction[1])
                pred = (ball[0] + direction[0], ball[1] + direction[1])

            else:
                # print('5')
                # No bounce, keep going
                pred = (ball[0] + direction[0], ball[1] + direction[1])
                self.predicted_ball = pred
                return

            if self.tiles[pred] in OBSTACLES:
                # print("!")
                prev = (ball[0] - direction[0], ball[1] - direction[0])
            else:
                # print("*")
                self.predicted_ball = pred
                return
                # prev, ball = ball, pred

    def process(self, x, y, id):
        prediction = 0
        if x == -1 and y == 0:
            self.score = id

        else:
            t = Tile(id)
            prev_tile = self.tiles[(x, y)]
            self.tiles[(x, y)] = t

            if Tile.BALL in self.tiles.values() and t is Tile.BALL:
                if t is Tile.BALL:
                    if not self.ball or not self.previous_ball:
                        self.ball = self.previous_ball = (x, y)

                    prev = self.ball
                    self.ball = (x, y)
                    # if self.ball != self.previous_ball:
                    self.previous_ball = prev

                if self.skip_prediction:
                    self.skip_prediction = False
                else:
                    prediction = self.make_prediction()
                    # if self.previous_ball == self.predicted_ball and not self.previous_ball == self.ball:
                    #     self.previous_ball = self.ball
                    #     prediction = self.make_prediction()

            # elif t is Tile.EMPTY and prev_tile is Tile.BLOCK:
            #     # print(f'gone: {x}, {y}')
            #     # self.previous_ball = (x,y)
            #     # self.predicted_ball = self.ball
            #     # self.skip_prediction = True

            elif t is Tile.PADDLE:
                prediction = self.make_prediction()
                self.previous_paddle, self.paddle = self.paddle, (x, y)
            #
            #
            # if t is Tile.EMPTY:
            #     self.cleared = (x,y)

        self.seen_direction = self.seen_direction or (self.direction is not None)

        # print(self.paddle, self.previous_ball, self.ball, self.predicted_ball, self.direction, prediction, self.seen_direction)
        print(self)
        if self.paddle and self.predicted_ball and self.seen_direction:
            if self.predicted_ball[0] == self.ball[0]:
                self.paddle_tilt = 0
            elif self.paddle[0] < self.predicted_ball[0]:
                self.paddle_tilt = 1
            elif self.paddle[0] > self.predicted_ball[0]:
                self.paddle_tilt = -1
            else:
                self.paddle_tilt = 0
            print("\n" * 4)
            # sleep(0.05)
            # print(self.ball[0], self.paddle[0], self.paddle_tilt)


if __name__ == "__main__":
    import sys
    import faulthandler

    # faulthandler.dump_traceback_later(10, True)

    lines = sys.stdin.readlines()
    program = IntcodeComputer.read_input(lines[0])
    program[0] = 2

    oq = queue.Queue(1)
    iq = queue.Queue(1)
    ready = threading.Condition()

    arcade = Arcade(oq, iq, ready)
    blah = Blah(arcade, ready, iq)
    computer = IntcodeComputer(program, iq, oq, ready)

    arcade_thread = threading.Thread(target=arcade.run, name="Arcade")
    computer_thread = threading.Thread(target=computer.run, name="Computer")
    blah_thread = threading.Thread(target=blah.run, name="Blah", daemon=True)

    blah_thread.start()
    computer_thread.start()
    arcade_thread.start()

    computer_thread.join()
    oq.put(None)
    arcade_thread.join()

    # print(arcade)

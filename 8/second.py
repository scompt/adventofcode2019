#!/usr/bin/env python

import sys

import numpy as np

data = sys.stdin.readlines()[0].strip()
width = int(sys.argv[1])
height = int(sys.argv[2])
layer_count = len(data) // width // height
parsed = np.array([int(d) for d in data]).reshape(layer_count, height, width)

for y in range(height):
    for x in range(width):
        for z in range(layer_count):
            if parsed[z, y, x] == 0:
                print("█", end="")
                break
            elif parsed[z, y, x] == 1:
                print(" ", end="")
                break
    print()

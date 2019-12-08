#!/usr/bin/env python

import sys

import numpy as np

data = sys.stdin.readlines()[0].strip()
width = int(sys.argv[1])
height = int(sys.argv[2])
layer_count = len(data) // width // height
parsed = np.array([int(d) for d in data]).reshape(layer_count, height, width)
fewest_nonzero_layer = np.argmax(
    [len(np.argwhere(parsed[i] > 0)) for i in range(len(parsed))]
)
product = len(np.argwhere(parsed[fewest_nonzero_layer] == 1)) * len(
    np.argwhere(parsed[fewest_nonzero_layer] == 2)
)
print(product)

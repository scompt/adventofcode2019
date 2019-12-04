#!/usr/bin/env python

from collections import defaultdict

count = 0
for n in range(254032, 789860):
    s = str(n)
    digits = defaultdict(lambda: 0)
    adjacent = False
    ascending = True
    for d in s:
        digits[d] += 1

    for l in range(len(s)-1):
        c1 = s[l:l+1]
        c2 = s[l+1:l+2]
        adjacent = (c1 == c2) or adjacent
        ascending = (int(c1) <= int(c2)) and ascending

    if adjacent and ascending:
        count += 1

print(count)

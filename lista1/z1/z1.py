#!/usr/bin/python3

import math
import random
from copy import copy
from threading import Timer

timeout = False
RANGE = 5
TWEAK = 5
ITERS = 20


def done():
    global timeout
    timeout = True


def h(x):
    mode2 = 0
    sum_el = 0
    for i in range(len(x)):
        mode2 += x[i] ** 2
        sum_el += x[i]
    return ((mode2 - 4) ** 2) ** 0.125 + 0.25 * (0.5 * mode2 + sum_el) + 0.5


def g(x):
    mode2 = 0
    product = 1
    for i in range(len(x)):
        mode2 += x[i] ** 2
        product *= math.cos(x[i] / (i + 1) ** 0.5)
    return 1 + 0.00025 * mode2 - product


def generate_point():
    return tuple(random.uniform(-2, 0) for _ in range(4))


def local_search(f):
    p = generate_point()
    p_cost = f(p)
    min = p
    min_cost = p_cost
    while not timeout:
        for _ in range(ITERS):
            newp = [x + random.gauss(0, 0.1) for x in p]
            newp_cost = f(newp)
            if newp_cost < p_cost:
                p = tuple(newp)
                p_cost = newp_cost
        if p_cost < min_cost:
            min = p
            min_cost = p_cost
        p = generate_point()
    return min, min_cost


def main():
    t, b = (int(i) for i in input().split())
    if b == 0:
        f = h
    else:
        f = g
    Timer(t, done).start()
    coords, f_val = local_search(f)
    for c in coords:
        print(c, end=" ")
    print(f_val)


if __name__ == "__main__":
    main()

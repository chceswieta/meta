import random
import numpy as np
from copy import copy
from time import time


def f(x):
    norm = np.linalg.norm(x)
    return 1 - np.cos(2 * np.pi * norm) + 0.1 * norm


def generate_next(current):
    #size = sum([abs(x) for x in current]) / 4 + 1e-10
    #return np.array([random.uniform(-size, size) for _ in range(4)])
    return np.array([x + random.gauss(0, 1) for x in current])

def global_minimum(start, start_temperature, cooling_rate, max_time):
    best = start, f(start)
    f_st = best[1]
    current = best
    temperature = start_temperature
    start_time = time()
    no_change = 0
    while time() - start_time < max_time and no_change < 1000000:
        new_x = generate_next(current[0])
        new_f = f(new_x)
        df = current[1] - new_f
        no_change += 1
        if df < 0 and temperature >= 0.1:
            P = np.exp(df / temperature)
            if P > random.random():
                current = new_x, new_f
        else:
            current = new_x, new_f
            if best[1] > new_f:
                no_change = 0
                best = copy(current)
        temperature *= cooling_rate
    return best


def main():
    in_data = [int(s) for s in input().split()]
    out_data = global_minimum(in_data[1:], 100, 0.99, in_data[0])
    print(*out_data[0], out_data[1])


if __name__ == "__main__":
    main()

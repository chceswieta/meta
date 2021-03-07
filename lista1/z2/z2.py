#!/usr/bin/python3

from copy import copy
from sys import stderr
from collections import deque
from time import time

timeout = False
distance_matrix = []
TABU_SIZE = 30


def full_cost(seq):
    cost = 0
    for i in range(len(distance_matrix)):
        cost += distance_matrix[seq[i]][seq[i + 1]]
    return cost


def relative_cost(base_seq, i, j):
    cost = base_seq[-1]
    cost -= distance_matrix[base_seq[i - 1]][base_seq[i]]
    cost -= (
          distance_matrix[base_seq[j - 1]][base_seq[j]]
        + distance_matrix[base_seq[j]][base_seq[j + 1]]
    )
    cost += (
          distance_matrix[base_seq[i - 1]][base_seq[j]]
        + distance_matrix[base_seq[i]][base_seq[j + 1]]
    )
    if i == j-1:
        cost += distance_matrix[base_seq[j]][base_seq[i]]
    else:
        cost += (
              distance_matrix[base_seq[j]][base_seq[i + 1]]
            + distance_matrix[base_seq[j - 1]][base_seq[i]]
        )
        cost -= distance_matrix[base_seq[i]][base_seq[i + 1]]
    return cost


def neighbours(seq, n):
    neighbours = [(i, j) for i in range(1, n - 1) for j in range(i + 1, n)]
    neighbours.sort(key=lambda s: relative_cost(seq, s[0], s[1]))
    return neighbours


def generate_first_path(n):
    seq = [0]
    psb = list(range(1, n))
    for i in range(n - 1):
        row = seq[-1]
        psb.sort(key=lambda p: distance_matrix[row][p])
        seq.append(psb.pop(0))

    seq += [0]
    seq.append(full_cost(seq))
    return seq


def tabu_search(n, max_time):
    seq = generate_first_path(n)
    min = [*seq]
    tabu = deque()
    no_change = 0
    start_time = time()
    while max_time > time() - start_time and no_change < 1000:
        no_change += 1
        for (i, j) in neighbours(seq, n):
            swap = tuple(sorted([seq[i], seq[j]]))
            if swap in tabu and relative_cost(seq, i, j) >= min[-1]:
                continue
            else:
                tabu.append(swap)
                seq[-1] = relative_cost(seq, i, j)
                seq[i], seq[j] = seq[j], seq[i]
                if seq[-1] < min[-1]:
                    min = [*seq]
                    no_change = 0
                break

        if len(tabu) > TABU_SIZE:
            tabu.popleft()
    return min


def main():
    global distance_matrix
    t, n = (int(i) for i in input().split())
    distance_matrix = [[int(d) for d in input().split()] for i in range(n)]
    result = tabu_search(n, t)
    print(result[-1])
    for s in result[:-1]:
        print(s + 1, file=stderr, end=" ")
    print("", file=stderr)


if __name__ == "__main__":
    main()

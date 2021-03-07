#!/usr/bin/python3

from copy import copy
from sys import stderr
from collections import deque
from time import time

board = []
TABU_SIZE = 5
start_pos = None
moves = {"L": (0, -1), "U": (-1, 0), "R": (0, 1), "D": (1, 0)}


def cost(seq, spos=start_pos):
    x, y = spos
    cost = 0
    legal_move_chunk = str()
    for s in seq:
        dx, dy = moves.get(s)
        if board[x + dx][y + dy] != "1":
            x += dx
            y += dy
            cost += 1
            legal_move_chunk += s
            if board[x][y] == "8":
                break
    else:
        cost = float("inf")
    return legal_move_chunk, cost


def generate_first_path():
    x, y = start_pos
    walk = str()
    options = {"L": ("D", "U"), "U": ("L", "R"), "R": ("U", "D"), "D": ("R", "L")}
    s = "L"
    cost = 0
    while True:
        v = options.get(s)
        dx, dy = moves.get(s)
        look_x, look_y = moves.get(v[0])
        while board[x + dx][y + dy] == "0":
            walk += s
            cost += 1
            x += dx
            y += dy
            if board[x + look_x][y + look_y] == "8":
                walk += v[0]
                cost += 1
                return walk, cost
        s = v[1]


def neighbours(seq: str):
    neighbours = set()
    base_cost = 0
    x, y = start_pos
    for i in range(len(seq)):
        for j in range(i + 1, len(seq)):
            if seq[i] != seq[j]:
                nb = seq[j] + seq[i+1 : j] + seq[i] + seq[j+1 :]
                nb, partial_cost = cost(nb, (x, y))
                neighbours.add((seq[:i] + nb, base_cost + partial_cost))
        dx, dy = moves.get(seq[i])
        x += dx
        y += dy
        base_cost += 1

    neighbours = list(neighbours)
    neighbours.sort(key=lambda s: s[1])
    return neighbours[:TABU_SIZE]


def tabu_search(max_time):
    seq, s_cost = generate_first_path()
    min, m_cost = seq, s_cost
    tabu = deque()
    no_change = 0
    start_time = time()
    while max_time > time() - start_time and no_change < 10000:
        for (n, c) in neighbours(seq):
            no_change += 1
            if n not in tabu or c < m_cost:
                if c < m_cost:
                    min = n
                    m_cost = c
                    no_change = 0
                tabu.append(n)
                s_cost = c
                seq = n
                break

        if len(tabu) > TABU_SIZE:
            tabu.popleft()
    return min, m_cost


def main():
    global board, start_pos
    t, n, m = (int(i) for i in input().split())
    board = [input() for i in range(n)]
    for i in range(n):
        try:
            start_pos = (i, board[i].index("5"))
            board[i] = board[i].replace("5", "0")
            break
        except ValueError:
            continue
    sequence, cost = tabu_search(t)
    print(cost)
    print(sequence, file=stderr)


if __name__ == "__main__":
    main()

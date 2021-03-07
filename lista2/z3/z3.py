from sys import stderr
from time import time
from random import randrange, random
from math import exp, inf

moves = [(0, -1), (-1, 0), (0, 1), (1, 0)]


class Board:
    def __init__(self, board, n, m):
        self.map = board
        self.max_path = n * m
        for i, row in enumerate(self.map):
            j = row.find("5")
            if j != -1:
                self.start = (i, j)
                break


    def find_exit(self, start_position, main_direction=0):
        x, y = start_position
        path = []
        while len(path) < self.max_path:
            dx, dy = moves[main_direction]
            ch_x, ch_y = moves[main_direction - 1]
            while self.map[x + dx][y + dy] != "8" and self.map[x + dx][y + dy] != "1":
                if self.map[x + ch_x][y + ch_y] == "8":
                    path.append((ch_x, ch_y))
                    return path
                x += dx
                y += dy
                path.append((dx, dy))

            if self.map[x + dx][y + dy] == "8":
                path.append((dx, dy))
                break

            cur_dir = (main_direction + 1) % 4
            has_turned = False
            while cur_dir != main_direction:
                dx, dy = moves[cur_dir]
                ch_x, ch_y = moves[cur_dir - 1]
                moves_made = 0
                while has_turned or self.map[x + ch_x][y + ch_y] == "1":
                    has_turned = False
                    next_key = self.map[x + dx][y + dy]
                    if next_key == "1":
                        alt_x, alt_y = moves[main_direction - 1]
                        if moves_made == 0 and cur_dir == (main_direction + 1) % 4 and self.map[x + alt_x][y + alt_y] == "0":
                            x += alt_x
                            y += alt_y
                            path.append((alt_x, alt_y))
                            cur_dir = main_direction - 1 
                        else:
                            cur_dir += 1
                        break
                    else:
                        moves_made += 1
                        x += dx
                        y += dy
                        path.append((dx, dy))
                        if next_key == "8":
                            return path
                else:
                    cur_dir -= 1
                    has_turned = True
                cur_dir %= 4
        return path

    def cost(self, path):
        if len(path) == self.max_path:
            return inf

        x, y = self.start
        steps_made = 0
        for dx, dy in path:
            steps_made += 1
            next_key = self.map[x + dx][y + dy]
            if next_key == "8":
                return steps_made
            elif next_key != "1":
                x += dx
                y += dy
        else:
            return steps_made + self.max_path

    def prefix_neighbour(self, path):
        nb = path.copy()
        x, y = self.start
        start = len(nb) // 2
        for dx, dy in nb[:start]:
            next_key = self.map[x + dx][y + dy]
            if next_key != "1":
                x += dx
                y += dy
        nb[start:] = self.find_exit((x, y), randrange(0, 4))
        return nb

    @staticmethod
    def reversed_neighbour(path):
        nb = path.copy()
        i, j = randrange(0, len(nb)//2), randrange(len(nb)//2, len(nb))
        if i:
            nb[i:j] = nb[j-1 : i-1 : -1]
        else:
            nb[0:j] = nb[j-1 :: -1]

        if nb[i][0] + nb[i+1][0] == 0 and nb[i][1] + nb[i+1][1] == 0:
            nb.pop(i)
            nb.pop(i)
            j -= 2
            nb.extend([moves[randrange(0, 4)] for _ in range(2)])

        if nb[j][0] + nb[j-1][0] == 0 and nb[j][1] + nb[j-1][1] == 0:
            nb.pop(j-1)
            nb.pop(j-1)
            nb.extend([moves[randrange(0, 4)] for _ in range(2)])

        return nb


def shortest_path(board: Board, start_temperature, cooling_rate, max_time):
    current = board.find_exit(board.start)
    cur_cost = board.cost(current)
    best = current.copy()
    best_cost = cur_cost

    no_change = 0
    temperature = start_temperature
    start_time = time()
    while time() - start_time < max_time and no_change < 1000000:
        no_change += 1
        if no_change % 100 == 0:
            new = board.prefix_neighbour(current)
        else:
            new = board.reversed_neighbour(current)
        new_cost = board.cost(new)

        df = cur_cost - new_cost
        if df > 0 or (temperature > 0.01 and exp(df / temperature) > random()):
            current = new.copy()[:new_cost]
            cur_cost = new_cost
            if new_cost < best_cost:
                no_change = 0
                best = current.copy()
                best_cost = cur_cost

        temperature *= cooling_rate

    return best, best_cost


def decode(path):
    move_codes = {(0, -1): "L", (-1, 0): "U", (0, 1): "R", (1, 0): "D"}
    return "".join(move_codes[s] for s in path)


def main():
    time_max, n, m = (int(i) for i in input().split())
    board = Board([input()[:m] for _ in range(n)], n, m)
    path, cost = shortest_path(board, 1000, 0.99, time_max)
    print(cost)
    print(decode(path), file=stderr)


if __name__ == "__main__":
    main()

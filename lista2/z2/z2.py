import random
from numpy import exp
from copy import deepcopy
from time import time
from sys import stderr

possible_numbers = [0, 32, 64, 128, 160, 192, 223, 255]


class Block:
    def __init__(self, v_min, v_max, h_min, h_max, val):
        self.value = val
        self.horizontal = [h_min, h_max]
        self.vertical = [v_min, v_max]
        self.width = h_max - h_min
        self.height = v_max - v_min

    def __repr__(self):
        return "({}, {}, {})".format(self.vertical, self.horizontal, self.value)


class MatrixWrapper:
    def __init__(self, matrix: list, k: int):
        self.matrix = matrix
        self.dimensions = len(matrix), len(matrix[0])
        self.min_blocksize = k

    def distance(self, solution: list) -> int:
        result = [
            (self.matrix[i][j] - n.value) ** 2
            for sol in solution
            for n in sol
            for i in range(*n.vertical)
            for j in range(*n.horizontal)
        ]
        n, m = self.dimensions
        return 1 / (n * m) * sum(result)

    def generate_first_solution(self) -> list:
        n, m = self.dimensions
        k = self.min_blocksize
        h_bounds = [i * k for i in range(m // k)] + [m]
        v_bounds = [i * k for i in range(n // k)] + [n]
        solution = []

        for i in range(len(v_bounds) - 1):
            sol = []
            for j in range(len(h_bounds) - 1):
                v_cur, v_next = v_bounds[i], v_bounds[i + 1]
                h_cur, h_next = h_bounds[j], h_bounds[j + 1]
                item_count = (h_next - h_cur) * (v_next - v_cur)
                value = (
                    sum(sum(self.matrix[r][h_cur:h_next]) for r in range(v_cur, v_next))
                    / item_count
                )

                val_index = 0
                for t in [17, 49, 97, 145, 177, 208, 240]:
                    if value >= t:
                        val_index += 1
                    else:
                        break
                value = possible_numbers[val_index]
                sol.append(Block(v_cur, v_next, h_cur, h_next, value))
            solution.append(sol)
        return solution

    @staticmethod
    def intensity_neighbour(solution):
        neighbour = deepcopy(solution)
        x = random.randrange(0, len(neighbour))
        y = random.randrange(0, len(neighbour[0]))
        while neighbour[x][y].value == solution[x][y].value:
            neighbour[x][y].value = possible_numbers[random.randrange(0, 8)]
        return neighbour

    def resized_neighbour(self, solution):
        neighbour = deepcopy(solution)
        coords = [(t, x, y) for x in range(len(neighbour)) for y in range(len(neighbour[x])) for t in ["w", "h"]]
        random.shuffle(coords)
        for t, x, y in coords:
            n = neighbour[x][y]
            if t == "w" and n.width > self.min_blocksize:
                if y > 0 and neighbour[x][y - 1].vertical == n.vertical:
                    neighbour[x][y - 1].horizontal[1] += 1
                    neighbour[x][y - 1].width += 1
                    neighbour[x][y].horizontal[0] += 1
                    neighbour[x][y].width -= 1
                    break
                elif y < len(neighbour[x]) - 1 and neighbour[x][y + 1].vertical == n.vertical:
                    neighbour[x][y + 1].horizontal[0] -= 1
                    neighbour[x][y + 1].width += 1
                    neighbour[x][y].horizontal[1] -= 1
                    neighbour[x][y].width -= 1
                    break
            elif t == "h" and n.height > self.min_blocksize:
                if x > 0 and neighbour[x - 1][y].horizontal == n.horizontal:
                    neighbour[x - 1][y].vertical[1] += 1
                    neighbour[x - 1][y].height += 1
                    neighbour[x][y].vertical[0] += 1
                    neighbour[x][y].height -= 1
                    break
                elif x < len(neighbour) - 1 and neighbour[x + 1][y].horizontal == n.horizontal:
                    neighbour[x + 1][y].vertical[0] -= 1
                    neighbour[x + 1][y].height += 1
                    neighbour[x][y].vertical[1] -= 1
                    neighbour[x][y].height -= 1
                    break
        return neighbour

    @staticmethod
    def swap_neighbour(solution):
        neighbour = deepcopy(solution)
        coords = [(x, y) for x in range(len(neighbour)) for y in range(len(neighbour)) if x != y]
        random.shuffle(coords)
        for x, y in coords:
            h = neighbour[x][0].height
            x_ver = neighbour[x][0].vertical
            if h != neighbour[y][0].height:
                continue
            y_ver = neighbour[y][0].vertical
            eligible = True
            for nx in neighbour[x]:
                if nx.vertical != x_ver:
                    eligible = False
                else:
                    nx.vertical = y_ver
            if eligible:
                for ny in neighbour[y]:
                    if ny.vertical != y_ver:
                        eligible = False
                    else:
                        ny.vertical = x_ver
                if eligible:
                    neighbour[x], neighbour[y] = neighbour[y], neighbour[x]
                return neighbour
        return solution


def approximate(matrix: MatrixWrapper, start_temperature, cooling_rate, max_time):
    current = matrix.generate_first_solution()
    cur_cost = matrix.distance(current)
    best = current.copy()
    best_cost = cur_cost
    no_change = 0
    temperature = start_temperature
    start_time = time()
    while time() - start_time < max_time and no_change < 10000:
        for neighbour in [matrix.intensity_neighbour, matrix.resized_neighbour, matrix.swap_neighbour]:
            new = neighbour(current)
            new_cost = matrix.distance(new)
            df = cur_cost - new_cost
            if df > 0 or (
                temperature > 0.1 and exp(df / temperature) > random.random()
            ):
                current = new.copy()
                cur_cost = new_cost
                if new_cost < best_cost:
                    no_change = 0
                    best = new.copy()
                    best_cost = new_cost
            else:
                no_change += 1
            temperature *= cooling_rate
    return best, best_cost


def matrixify(solution, n, m):
    for i in range(n):
        pr = [s for sol in solution for s in sol if s.vertical[0] <= i < s.vertical[1]]
        pr.sort(key=lambda s: s.horizontal[0])
        for s in pr:
            for j in range(s.horizontal[0], s.horizontal[1]):
                print("{:3}".format(s.value), end=" ", file=stderr)
        print(file=stderr)


def main():
    time_max, n, m, k = (int(i) for i in input().split())
    input_mx = [[int(i) for i in input().split()[:m]] for _ in range(n)]
    matrix = MatrixWrapper(input_mx, k)
    res, res_dist = approximate(matrix, 100, 0.95, time_max)
    print(res_dist)
    matrixify(res, n, m)


if __name__ == "__main__":
    main()

import random
from sys import stderr
from time import time
from copy import deepcopy, copy

moves = [(0, -1), (-1, 0), (0, 1), (1, 0)]

class Path:
    def __init__(self, dirs):
        self.path = dirs
        self.cost = None

    def mutate(self):
        child = deepcopy(self)
        child.cost = None
        mutated = False
        for i in range(len(self.path)):
            if 0.25 >= random.random():
                child.path[i] = random.choice(moves)
                mutated = True
        return child if mutated else self

    def __repr__(self):
        return str(self.cost)

class Board:
    def __init__(self, board, n, m, start_pop, pop_size):
        self.map = board
        self.max_path = n * m
        for i, row in enumerate(self.map):
            j = row.find("5")
            if j != -1:
                self.start = (i, j)
                break
        self.pop_size = pop_size
        self.start_pop = [self.create_path(p) for p in start_pop]
        for _ in range(pop_size - 4):
            self.start_pop.append(self.create_path([moves[random.randrange(0,4)] for _ in range(self.max_path-1)]))

    def create_path(self, step_list):
        p = Path(step_list)
        p.cost = self.cost(p)
        p.path = p.path[:p.cost]
        return p

    def cost(self, path):
        path = path.path

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

    def select(self, population):
        picks = random.sample(population, k=2)
        return min(picks, key=lambda w: w.cost)

    def crossover(self, p1, p2):
        i = random.randrange(0, len(p1.path))
        j = random.randrange(0, len(p2.path))
        
        c1 = p1.path.copy()
        c2 = p2.path.copy()

        c1[i:], c2[j:] = c2[j:], c1[i:]
        return Path(c1), Path(c2)

    def survivors(self, population):
        for p in population:
            if not p.cost:
                p.cost = self.cost(p)
                p.path = p.path[:p.cost]
        random.shuffle(population)
        groups = [population[i::self.pop_size] for i in range(self.pop_size)]
        survivors = [min(g, key=lambda p: p.cost) for g in groups]
        return survivors

    def shortest_path(self, max_time):
        population = self.start_pop.copy()
        best = None

        no_change = 0
        start_time = time()
        while time() - start_time < max_time and no_change < 10000:
            no_change += 1
            for p in population:
                if best is None or p.cost < best.cost:
                    best = copy(p)
                    no_change = 0

            next_gen = population.copy()
            for _ in range(self.pop_size // 2):
                p1 = self.select(population)
                p2 = self.select(population)
                c1, c2 = self.crossover(p1, p2)
                next_gen += [c1.mutate(), c2.mutate()]
            population = self.survivors(next_gen)
        return best


def convert(path, encode=False):
    if encode:
        move_codes = {"L": (0, -1), "U": (-1, 0),"R": (0, 1), "D": (1, 0)}
        return [move_codes[s] for s in path]
    else:
        move_codes = {(0, -1): "L", (-1, 0): "U", (0, 1): "R", (1, 0): "D"}
        return "".join(move_codes[s] for s in path)


def main():
    t, n, m, s, p = (int(i) for i in input().split())
    board_map = [input()[:m] for _ in range(n)]
    start_pop = [convert(input().strip(), encode=True) for _ in range(s)]
    board = Board(board_map, n, m, start_pop, p)
    path = board.shortest_path(t)
    print(path.cost)
    print(convert(path.path), file=stderr)


if __name__ == "__main__":
    main()

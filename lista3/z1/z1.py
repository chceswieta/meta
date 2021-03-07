from random import random
from time import time
import numpy as np


class Particle:
    velocity_retention = 0.5
    personal_factor = 2
    global_factor = 3

    def __init__(self, start, start_fitness, fitness_func):
        self.cur_pos = start.copy()
        self.cur_fit = start_fitness
        self.velocity = np.random.normal(0, 1, 5)

        self.best_pos = start.copy()
        self.best_fit = start_fitness

        self.fitness = fitness_func

    def update_fitness(self):
        self.cur_fit = self.fitness(self.cur_pos)
        if self.cur_fit < self.best_fit:
            self.best_fit = self.cur_fit
            self.best_pos = self.cur_pos.copy()

    def update_velocity(self, global_best_pos):
        retained_vel = random() * self.velocity_retention * self.velocity
        personal_vel = random() * self.personal_factor * (self.best_pos - self.cur_pos)
        global_vel = random() * self.global_factor * (global_best_pos - self.cur_pos)
        self.velocity = retained_vel + personal_vel + global_vel

    def update_position(self):
        self.cur_pos += self.velocity
        self.cur_pos[self.cur_pos > 5] = 5
        self.cur_pos[self.cur_pos < -5] = -5


def particle_swarm_optimization(start, fitness, max_time, swarm_size):
    global_best_pos = start
    global_best_fit = fitness(start)
    swarm = [Particle(start, global_best_fit, fitness) for _ in range(swarm_size)]

    start_time = time()
    while time() - start_time < max_time:
        for particle in swarm:
            particle.update_position()

            particle.update_fitness()
            if particle.cur_fit < global_best_fit:
                global_best_fit = particle.cur_fit
                global_best_pos = particle.cur_pos.copy()

        for particle in swarm:
            particle.update_velocity(global_best_pos)

    return global_best_pos, global_best_fit


def main():
    in_data = input().split()[:11]
    t = int(in_data[0])
    x = np.array([int(c) for c in in_data[1:6]], dtype=float)
    epsilon = np.array([float(e) for e in in_data[6:]])
    xs_yang = lambda x: np.sum(np.abs(x) ** (range(1, 6)) * epsilon)
    pos, fit = particle_swarm_optimization(x, xs_yang, t, 20)
    print(" ".join(str(p) for p in pos), fit)


if __name__ == "__main__":
    main()

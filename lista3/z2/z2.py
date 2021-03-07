import random
from time import time
from sys import stderr

class GeneticAlgorithm:
    def __init__(self, alphabet, dictionary, samples, pop_size=20, mutation_chance=0.25, extension_chance=0.75, extension_factor=0.5):
        self.alphabet = alphabet
        self.dictionary = dictionary
        letter_pool = []
        for ch in alphabet:
            letter_pool += alphabet[ch][1] * [ch]

        self.start_population = samples
        for _ in range(pop_size - len(samples)):
            random.shuffle(letter_pool)
            while True:
                new_word = "".join(letter_pool[:random.randint(1, len(letter_pool))])
                if new_word not in self.start_population: break
            self.start_population.append(new_word)
        self.pop_size = pop_size

        self.mutation_chance = mutation_chance
        self.extension_chance = extension_chance
        self.extension_factor = extension_factor

    def fitness(self, word):
        try:
            return self.dictionary[word]
        except KeyError:
            return 0

    def select_parent(self, population):
        picks = random.sample(population, k=2)
        return max(picks, key=lambda w: self.fitness(w))

    def hunger_games(self, population):
        random.shuffle(population)
        groups = [population[i::self.pop_size] for i in range(self.pop_size)]
        survivors = [max(g, key=lambda w: self.fitness(w)) for g in groups]
        return survivors

    def crossover(self, p1, p2):
        limit = min(len(p1), len(p2))
        i = random.randrange(0, len(p1))
        j = random.randrange(0, len(p2))

        c1 = list(p1)
        c2 = list(p2)
        c1[i:], c2[j:] = c2[j:], c1[i:]

        return "".join(c1), "".join(c2)

    def mutate(self, c):
        chars = list(c)
        available = [ch for ch in self.alphabet.keys() if chars.count(ch) < self.alphabet[ch][1]]
        if available:
            for i in range(len(c)):
                if self.mutation_chance >= random.random():
                    cur_char = chars[i]
                    chars[i] = random.choice(available)
                    available.remove(chars[i])
                    available.append(cur_char)

            extension_probabilty = self.extension_chance
            while available:
                if extension_probabilty >= random.random():
                    new_char = random.choice(available)
                    chars.append(new_char)
                    available.remove(new_char)
                    extension_probabilty *= self.extension_factor
                else:
                    break
        else:
            random.shuffle(chars)

        return "".join(chars)


    def run(self, max_time):
        population = self.start_population.copy()
        best = population[0]
        
        no_change = 0
        while time() < max_time and no_change < 10000:
            no_change += 1
            for p in population:
                if self.fitness(p) > self.fitness(best):
                    no_change = 0
                    best = p
            next_gen = population.copy()
            for _ in range(self.pop_size):
                p1 = self.select_parent(population)
                p2 = self.select_parent(population)
                c1, c2 = self.crossover(p1, p2)
                next_gen.extend([self.mutate(c1), self.mutate(c2)])
            population = self.hunger_games(next_gen)

        return best

def main():
    start_time = time()
    t, n, s = (int(w) for w in input().split())
    alphabet = [(line[0], int(line[1])) for _ in range(n) if (line := input().split())]
    alphabet = {
        ch: (pt, alphabet.count((ch, pt))) for ch, pt in alphabet
    }
    start_population = [input().lower().strip() for _ in range(s)]
    with open("dict.txt") as f:
        dictionary = {
            word: fitness
            for line in f.readlines()
            if (word := line.strip().lower())
            and all(
                [
                    char in alphabet and word.count(char) <= alphabet[char][1]
                    for char in word
                ]
            )
            and (fitness := sum(alphabet[char][0] for char in word))
        }
    model = GeneticAlgorithm(alphabet, dictionary, start_population)
    word = model.run(start_time + t)
    print(model.fitness(word))
    print(word, file=stderr)


if __name__ == "__main__":
    main()

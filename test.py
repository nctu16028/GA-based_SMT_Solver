import numpy as np
import matplotlib.pyplot as plt
from sys import argv
from utils import prim


class GeneticAlgorithm():
    def __init__(self, h: int, w: int, pins: np.ndarray, size: int) -> None:
        self.board_h = h
        self.board_w = w
        self.pinMap = pins
        self.chromosome_length = len(pins)
        self.population_size = size
        self.population = []
        self.fitness = []
        self.history = []

    def run(self, num_generations: int, selection_scheme: int) -> int:
        self._initialization()
        optimum = self._evaluation()
        print("Best fitness:", self.fitness[optimum])
        print("Lowest MST cost:", 2 * self.board_h * self.board_w - self.fitness[optimum])
        self.history.append(2 * self.board_h * self.board_w - self.fitness[optimum])
        for _ in range(num_generations):
            print("Gen", _ + 1)
            mating_pool = self._parent_selection(selection_scheme)
            offspring = self._recombination(mating_pool)
            self._mutation(offspring, 0.1)
            self._replacement(offspring)
            optimum = self._evaluation()
            print("Best fitness:", self.fitness[optimum])
            print("Lowest MST cost:", 2 * self.board_h * self.board_w - self.fitness[optimum])
            self.history.append(2 * self.board_h * self.board_w - self.fitness[optimum])
        return optimum
        
    def _initialization(self) -> None:
        for _ in range(self.population_size):
            chromosome = np.random.randint(low=0, high=2, size=self.chromosome_length)
            self.population.append(chromosome)
            self.fitness.append(0)

    def _evaluation(self) -> int:
        best_fitness = -np.inf
        best_indie = -1
        for i in range(self.population_size):
            self.fitness[i] = calculate_fitness(self.board_h, self.board_w, self.pinMap, self.population[i])
            if self.fitness[i] > best_fitness:
                best_fitness = self.fitness[i]
                best_indie = i
        return best_indie

    def _parent_selection(self, scheme: int) -> list:
        mating_pool = []
        for _ in range(self.population_size):
            if scheme == 0:
                candidate = self.__drawOneByRouletteWheel()
            elif scheme == 1:
                candidate = self.__drawOneByTournament()
            mating_pool.append(self.population[candidate])
        return mating_pool
    
    def _recombination(self, pool: list, pc: float = 1.0) -> list:
        offspring = []
        while len(pool) >= 2:
            parent1 = pool.pop()
            parent2 = pool.pop()
            if np.random.rand() < pc:   # 1-point crossover with probability pc
                split = np.random.randint(low=1, high=50)
                child1 = np.concatenate((parent1[:split], parent2[split:]))
                child2 = np.concatenate((parent2[:split], parent1[split:]))
            else:
                child1 = parent1
                child2 = parent2
            offspring.append(child1)
            offspring.append(child2)
        while len(pool) > 0:
            offspring.append(pool.pop())
        return offspring

    def _mutation(self, offspring: list, pm: float = 0.0) -> None:
        for i in range(len(offspring)):
            for j in range(len(offspring[i])):
                if np.random.rand() < pm:   # bitwise mutation with probability pm
                    offspring[i][j] = 0
                    #offspring[i][j] = 1 - offspring[i][j]

    def _replacement(self, offspring: list) -> None:
        self.population = offspring

    def __drawOneByRouletteWheel(self) -> int:
        sign = np.random.randint(low=0, high=sum(self.fitness))
        i = 0
        while sign >= self.fitness[i]:
            sign -= self.fitness[i]
            i += 1
        return i

    def __drawOneByTournament(self, tournament_size: int = 2) -> int:
        competitors_indices = np.random.choice(self.population_size, size=tournament_size, replace=False)
        competitors_fitness = np.array(self.fitness)[competitors_indices]
        winner_index = competitors_indices[np.argmax(competitors_fitness)]
        return winner_index


def calculate_fitness(h: int, w: int, pinMap: np.ndarray, steinerMap: np.ndarray) -> int:
    upperbound = 2 * h * w
    vertices = np.nonzero(pinMap | steinerMap)[0]
    cost = prim(w, vertices)
    return upperbound - cost


def visualization(chart: list, pinMap2D: np.ndarray, steinerMap2D: np.ndarray) -> None:
    plt.plot(chart, 'ro-')
    plt.xlabel('Generations')
    plt.ylabel('MST cost')
    plt.title(argv[1])
    plt.show()

    plt.grid(True, linestyle='--',)
    y_indices, x_indices = np.where(steinerMap2D == 1)
    plt.scatter(x_indices, y_indices, marker='o', color='blue', label='Steiner points')
    y_indices, x_indices = np.where(pinMap2D == 1)
    plt.scatter(x_indices, y_indices, marker='o', color='red', label='Pins')
    xMax = steinerMap2D.shape[1]
    yMax = steinerMap2D.shape[0]
    plt.xticks(np.arange(0, xMax, 1))
    plt.yticks(np.arange(0, yMax, 1))
    plt.axis([-1, xMax, -1, yMax])
    plt.axis('equal')
    plt.legend()
    plt.title(argv[1])
    plt.show()


if __name__ == '__main__':
    if len(argv) < 2:
        raise Exception("Please specify the input data file")
    
    with open(argv[1], 'r') as file:
        lines = file.read().splitlines()
    board_dim = lines[0]
    pin_coords = lines[1:]

    board_height, board_width = [int(c) for c in board_dim.split()]
    pinMap = np.zeros(board_height * board_width, dtype=int)
    for coord in pin_coords:
        x, y = [int(c) for c in coord.split()]
        pinMap[x * board_width + y] = 1
    print(pinMap.reshape((board_height, board_width)))

    print(prim(board_width, np.nonzero(pinMap)[0]))

    solver = GeneticAlgorithm(board_height, board_width, pinMap, 200)
    optimum = solver.run(30, 1)
    print(solver.population[optimum].reshape((board_height, board_width)))
    print(solver.history)

    visualization(
        solver.history,
        pinMap.reshape((board_height, board_width)),
        solver.population[optimum].reshape((board_height, board_width))
    )

from itertools import product
from random import sample
import time

class Population:
    def __init__(self, width, height, living=set()):
        self.width = width
        self.height = height
        self.living = living

    def neighbors(self, cell):
        x, y = cell
        not_self = lambda c: c != cell
        inbounds_width = lambda c: 0 <= c[0] < self.width
        inbounds_height = lambda c: 0 <= c[1] < self.height

        result = product(range(x - 1, x + 2), range(y - 1, y + 2))
        result = filter(not_self, result)
        result = filter(inbounds_width, result)
        result = filter(inbounds_height, result)
        result = filter(lambda c: c in self.living, result)
        return list(result)

    def __str__(self):
        grid_str = ''
        for y in range(self.height):
            for x in range(self.width):
                grid_str += '*' if (x, y) in self.living else ' '
            grid_str += '\n'
        return grid_str
    
    @staticmethod
    def random(width, height, p_alive):
        all_cells = list(product(range(width), range(height)))
        num_alive = int(p_alive * width * height)
        alive = set(sample(all_cells, num_alive))
        return Population(width, height, alive)

def GameOfLife(population, N=100):
    while N > 0:
        all_cells = product(range(population.width), range(population.height))
        new_living_set = set()
        for cell in all_cells:
            alive = cell in population.living
            num_neighbors = len(population.neighbors(cell))

            if alive and 1 < num_neighbors < 4:
                new_living_set.add(cell)
            if not alive and num_neighbors == 3:
                new_living_set.add(cell)
        
        print(population.living)
        yield population
        N -= 1
        population.living= new_living_set

if __name__ == '__main__':
    p = Population(50, 20)
    p.living = set([(2, 1), (3, 2), (1, 3), (2, 3), (3, 3)])
    game = GameOfLife(p)

    for generation, state in enumerate(game):
        print(state)
        print('%s%d%s' % ('-'*25, generation, '-'*25))
        time.sleep(.1)
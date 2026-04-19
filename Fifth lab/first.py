import pygad
import math

N, M, R = map(float, input().split())
N = int(N)
M = int(M)

points = [tuple(map(float, input().split())) for _ in range(N)]

def dist(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def decode(solution):
    umbrellas = []

    for i in range(0, len(solution), 2):
        x = solution[i]
        y = solution[i + 1]
        umbrellas.append((x, y))

    return umbrellas

def fitness_func(ga, solution, idx):
    umbrellas = decode(solution)
    invalid_penalty = 0
    for x, y in umbrellas:
        if x - R < 0 or x + R > 10 or y - R < 0 or y + R > 10:
            invalid_penalty += 5000

    uncovered_penalty = 0

    for px, py in points:
        covered = False
        for ux, uy in umbrellas:
            if dist((px, py), (ux, uy)) <= R:
                covered = True
                break
        if not covered:
            uncovered_penalty += 1000

    large_overlap = 0
    small_overlap = 0

    for i in range(len(umbrellas)):
        for j in range(i + 1, len(umbrellas)):
            d = dist(umbrellas[i], umbrellas[j])

            if d > 2 * R:
                continue

            if d < (8*R)/5:
                large_overlap += 1
            else:
                small_overlap += 1


    overlap_penalty = large_overlap * 20 + small_overlap * 2

    usage_penalty = len(umbrellas) * 2

    total = uncovered_penalty + overlap_penalty + usage_penalty + invalid_penalty

    return -total

gene_space = []

for _ in range(M * 2):
    gene_space.append([i * 0.1 for i in range(0, 101)])

params = {
    'num_generations': 500,
    'sol_per_pop': 100,
    'num_parents_mating': 50,

    'num_genes': int(M * 2),
    'gene_space': gene_space,

    'fitness_func': fitness_func,

    'mutation_num_genes': 1,
    'save_best_solutions': True
}

ga = pygad.GA(**params)
ga.run()

solution, _, _ = ga.best_solution()
fitness = fitness_func(None, solution, 0)
best_solutions = ga.best_solutions


print(solution)
print(fitness)

chromosomes = [
    [20, 20, 20, 20, 20, 20],      # invalid (outside grid)
    [1, 1, 1.1, 1.1, 1.2, 1.2],    # heavy overlap, poor coverage
    [1, 1, 1.2, 1, 1.1, 1.2],      # covers cluster, misses (5,5)
    [1, 1, 1.1, 1, 5, 5],          # full coverage, some overlap
    [1, 1, 5, 5, 8, 8]             # best (minimal overlap, full coverage)
]
best_solutions_sorted = sorted(
    best_solutions,
    key=lambda sol: fitness_func(None, sol, 0),
    reverse=False
)
ss = sorted(
    chromosomes,
    key=lambda sol: fitness_func(None, sol, 0),
    reverse=False
)
#submit_data(fitness_func, decode, ss, best_solutions_sorted)
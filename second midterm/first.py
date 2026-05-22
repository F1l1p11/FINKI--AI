import pygad
import random
random.seed(0)

rooms = {
    1: {'name': 'Modern & Contemporary Art', 'adjacent': [2, 7], 'value': 110},
    2: {'name': 'European History', 'adjacent': [1, 3, 4, 5, 7], 'value': 130},
    3: {'name': 'Seasonal Exhibitions', 'adjacent': [2], 'value': 100},
    4: {'name': 'Prehistory', 'adjacent': [2, 6, 10], 'value': 140},
    5: {'name': 'Medieval Times', 'adjacent': [2, 6, 9], 'value': 120},
    6: {'name': 'Arms and Armor', 'adjacent': [4, 5], 'value': 150},
    7: {'name': 'Arts of Africa, Oceania and the Americas', 'adjacent': [1, 2, 8], 'value': 90},
    8: {'name': 'Greek and Roman History', 'adjacent': [7, 9], 'value': 180},
    9: {'name': 'The Great Hall', 'adjacent': [5, 8, 10], 'value': 30},
    10: {'name': 'Egyptian History', 'adjacent': [4, 9], 'value': 200}
}
K = int(input())

big_rooms = {2, 8, 9, 10}
def fitness_func(ga, solution, idx):
    total_cameras = sum(int(x) for x in solution)
    if total_cameras > K:
        return -1000000

    coverage = [0] * 11
    for room_id in range(1, 11):
        cameras = int(solution[room_id - 1])
        if cameras == 0:
            continue
        if room_id in big_rooms:
            coverage[room_id] += min(cameras * 60, 100)
        else:
            coverage[room_id] += 100
        for adj in rooms[room_id]['adjacent']:
            coverage[adj] += cameras * 10

    total_value = 0

    for room_id in range(1, 11):
        coverage[room_id] = min(coverage[room_id], 100)
        total_value += (rooms[room_id]['value'] * coverage[room_id] / 100)
    return total_value

gene_space = []

for i in range(10):
    if K == 1:
        gene_space.append([int(0),int(1)])
    else:
        if i + 1 in big_rooms:
            gene_space.append([int(0), int(1), int(2)])
        else:
            gene_space.append([int(0), int(1)])

params = {
    'num_generations': 1000,
    'sol_per_pop': 100,
    'num_parents_mating': 40,

    'num_genes': 10,
    'gene_space': gene_space,

    'fitness_func': fitness_func,

    'mutation_num_genes': 1,
    'random_seed': 0
}

ga = pygad.GA(**params)

ga.run()

best_solution, _, _ = ga.best_solution()
best_fitness = fitness_func(None, best_solution, 0)
print(f'Optimal protected value: {best_fitness}M$')
import pygad

N = int(input())
S, E = map(int, input().split())
dist = [list(map(float, input().split())) for _ in range(N)]

cities_to_visit = [i for i in range(N) if i != S and i != E]
num_cities_to_visit = len(cities_to_visit)


def decode(solution):
    if num_cities_to_visit == 0:
        return [S, E], [S, E]

    city_info = []

    for i in range(num_cities_to_visit):
        city = cities_to_visit[i]

        position = solution[2 * i]
        friend = int(round(solution[2 * i + 1]))

        # keep only valid genes
        if friend in [0, 1]:
            city_info.append((position, friend, city))
        # friend == 2 → skip

    city_info.sort(key=lambda x: x[0])

    f1, f2 = [], []

    for _, friend, city in city_info:
        if friend == 0:
            f1.append(city)
        elif friend == 1:
            f2.append(city)

    route1 = [S] + f1 + [E]
    route2 = [S] + f2 + [E]

    return route1, route2


def calculate_route_time(route):
    total_time = 0
    for i in range(len(route) - 1):
        total_time += dist[route[i]][route[i + 1]]
    return total_time


def fitness_func(ga, solution, idx):
    route1, route2 = decode(solution)

    visited = set(route1 + route2)
    required = set([S, E] + cities_to_visit)

    missing = required - visited

    time1 = calculate_route_time(route1)
    time2 = calculate_route_time(route2)

    fitness = max(time1, time2)

    # 🔴 VERY IMPORTANT: punish skipping cities
    fitness += 10000 * len(missing)

    if abs(len(route1) - len(route2)) > 0:
        fitness += 5 * abs(len(route1) - len(route2))

    return -fitness

gene_space = []
for i in range(num_cities_to_visit):
    gene_space.append({'low': 0, 'high': num_cities_to_visit - 1})
    gene_space.append([0, 1, 2])

params = {
    'num_generations': 500,
    'sol_per_pop': 100,
    'num_parents_mating': 50,
    'num_genes': num_cities_to_visit * 2,
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

route1, route2 = decode(solution)
print("Friend 1 route:", route1)
print("Friend 2 route:", route2)
print("Fitness:", fitness)

#submit_data(fitness_func, decode, best_solutions)
from constraint import Problem, BacktrackingSolver, AllDifferentConstraint
from itertools import combinations

def read_input():
    num_families = int(input())
    families = {}
    for _ in range(num_families):
        name, size, reqs_string, exact = input().split()
        reqs = reqs_string.split('-')
        families[name] = {'size': int(size), 'requirements': reqs, 'exact': exact}
    num_rooms = int(input())
    rooms = {}
    for _ in range(num_rooms):
        room_id, capacity, amenities_string = input().split()
        amenities = amenities_string.split('-')
        rooms[int(room_id)] = {'capacity': int(capacity), 'amenities': amenities}
    return families, rooms

def room_fits(room_id, family, rooms):
    room = rooms[room_id]

    # Check capacity constraint
    if family['exact']:
        # If exact is true, room capacity must equal family size
        if room['capacity'] != family['size']:
            return False
    else:
        # If exact is false, room capacity must be at least family size
        if room['capacity'] < family['size']:
            return False
    # Check amenities
    reqs = family['requirements']
    if reqs == ['none']:
        return True
    return all(req in room['amenities'] for req in reqs)

def is_valid(solution, all_families, rooms):
    assigned_rooms = set(solution.values())
    for name, family in all_families.items():
        if name not in solution:
            for room_id in rooms:
                if room_id not in assigned_rooms and room_fits(room_id, family, rooms):
                    return False
    return True

def solve_subset(subset, valid_rooms, families):
    if not subset:
        return [{}]
    problem = Problem(solver=BacktrackingSolver())
    for name in subset:
        problem.addVariable(name, valid_rooms[name])
    if len(subset) > 1:
        problem.addConstraint(AllDifferentConstraint(), list(subset))
    return problem.getSolutions()

if __name__ == '__main__':
    families, rooms = read_input()

    valid_rooms = {
        name: [r for r in rooms if room_fits(r, families[name], rooms)]
        for name in families
    }
    eligible = sorted(
        [n for n in families if valid_rooms[n]],
        key=lambda n: families[n]['size'],
        reverse=True
    )

    best = None
    best_score = -1

    for size in range(len(eligible), -1, -1):
        if best is not None:
            break
        for subset in combinations(eligible, size):
            solutions = solve_subset(list(subset), valid_rooms, families)
            for sol in solutions:
                if is_valid(sol, families, rooms):
                    score = sum(families[n]['size'] for n in sol)
                    if score > best_score:
                        best_score = score
                        best = sol
            if best is not None:
                break

    print("Best assignment:")
    if best:
        for name, room_id in sorted(best.items(), key=lambda x: x[1]):
            print(f"{name}->{room_id}")
from constraint import Problem, BacktrackingSolver, AllDifferentConstraint
from itertools import combinations


def read_input():
    num_families = int(input())
    families = {}
    for _ in range(num_families):
        name, size, reqs_string = input().split()
        reqs = reqs_string.split('-')
        families[name] = {'size': int(size), 'requirements': reqs}

    num_rooms = int(input())
    rooms = {}
    for _ in range(num_rooms):
        room_id, capacity, amenities_string = input().split()
        amenities = amenities_string.split('-')
        rooms[int(room_id)] = {'capacity': int(capacity), 'amenities': amenities}

    return families, rooms


def get_floor(room_id):
    """Extract floor number from room ID (first digit)"""
    return int(str(room_id)[0])


def room_fits(room_id, family, rooms):
    """Check if room meets basic capacity and amenity requirements"""
    room = rooms[room_id]
    if room['capacity'] < family['size']:
        return False
    reqs = family['requirements']
    if reqs == ['none']:
        return True
    return all(req in room['amenities'] for req in reqs)


def room_fits_perfectly(room_id, family, rooms):
    """Check if room meets requirements without flooding issues"""
    if not room_fits(room_id, family, rooms):
        return False

    floor = get_floor(room_id)
    reqs = family['requirements']

    # Floor 1: balcony issue
    if floor == 1 and 'balcony' in reqs:
        return False

    # Floor 4+: wifi issue
    if floor >= 4 and 'wifi' in reqs:
        return False

    return True


def is_valid(solution, all_families, rooms):
    """Validate that no guest is unjustifiably rejected"""
    assigned_rooms = set(solution.values())

    # Check basic constraint: no unjustified rejections
    for name, family in all_families.items():
        if name not in solution:
            # Check if there's any available room that fits
            for room_id in rooms:
                if room_id not in assigned_rooms and room_fits(room_id, family, rooms):
                    return False

    # Check flooding extension: prefer perfect rooms over compromised ones
    for name in solution:
        room_id = solution[name]
        family = all_families[name]
        floor = get_floor(room_id)
        reqs = family['requirements']

        # If assigned to floor 1 with balcony requirement
        if floor == 1 and 'balcony' in reqs:
            # Check if there's a better room (not floor 1) available
            for other_room in rooms:
                if other_room not in assigned_rooms and room_fits_perfectly(other_room, family, rooms):
                    return False

        # If assigned to floor 4+ with wifi requirement
        if floor >= 4 and 'wifi' in reqs:
            # Check if there's a better room (below floor 4) available
            for other_room in rooms:
                if other_room not in assigned_rooms and room_fits_perfectly(other_room, family, rooms):
                    return False

    return True


def solve_subset(subset, valid_rooms, families):
    """Solve CSP for a given subset of families"""
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

    # Find valid rooms for each family (basic fit, ignoring flooding)
    valid_rooms = {
        name: [r for r in rooms if room_fits(r, families[name], rooms)]
        for name in families
    }

    # Only consider families that have at least one valid room
    eligible = sorted(
        [n for n in families if valid_rooms[n]],
        key=lambda n: families[n]['size'],
        reverse=True
    )

    best = None
    best_score = -1

    # Try subsets from largest to smallest to maximize accommodated guests
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
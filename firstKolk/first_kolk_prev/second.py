from constraint import *

def adjacent_constraint(tent, tree):
    tr, tc = tree
    r, c = tent
    # Tent must be directly above, below, left, or right of the tree
    return (abs(tr - r) == 1 and tc == c) or (abs(tc - c) == 1 and tr == r)

def not_adjacent(*tents):
    # No two tents may touch, even diagonally
    for i in range(len(tents)):
        for j in range(i + 1, len(tents)):
            r1, c1 = tents[i]
            r2, c2 = tents[j]
            if abs(r1 - r2) <= 1 and abs(c1 - c2) <= 1:
                return False
    return True

if __name__ == '__main__':
    problem = Problem(BacktrackingSolver())

    # ----------------------------------------------------
    # --- Input: tree positions on the 6x6 board
    number = int(input())
    trees = []
    for i in range(number):
        temp = tuple(map(int, input().split()))
        trees.append(temp)
    # trees = [(0,1), (3,1), (5,1), (4,2), (3,3), (5,4), (2,5)]

    # All possible board positions (excluding trees)
    positions = [(r, c) for r in range(6) for c in range(6) if (r, c) not in trees]

    # -----------------------------------------------------
    # --- Variables: one tent per tree
    for i, tree in enumerate(trees):
        problem.addVariable(f"T{i}", positions)

    # -----------------------------------------------------
    # --- Constraints

    # Each tent must be adjacent to its tree
    for i, tree in enumerate(trees):
        problem.addConstraint(lambda tent, tree=tree: adjacent_constraint(tent, tree), [f"T{i}"])

    # All tents must be in different positions
    problem.addConstraint(AllDifferentConstraint(), [f"T{i}" for i in range(len(trees))])

    # No two tents may touch (not even diagonally)
    problem.addConstraint(not_adjacent, [f"T{i}" for i in range(len(trees))])

    # -----------------------------------------------------
    # --- Solve
    solution = problem.getSolution()

    # -----------------------------------------------------
    # --- Print tent positions
    if solution:
        for i, tree in enumerate(trees):
            # print(f"Tree {tree} -> Tent {solution[f'T{i}']}")
            r, c = solution[f"T{i}"]
            print(r, c)
    else:
        print("No solution found.")

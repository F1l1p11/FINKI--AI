from constraint import *


# helper: check how many tents are in a given column
def count_in_col_i(col_index, expected_count, variables):
    def constraint(*args):
        count = 0
        for (r, c) in args:
            if c == col_index:
                count += 1
        return count == expected_count

    return constraint


if __name__ == '__main__':
    problem = Problem(BacktrackingSolver())

    # ----------------------------------------------------
    # --- Read input -------------------------------------

    M = int(input())  # number of trees

    trees = []
    for _ in range(M):
        r, c = map(int, input().split())
        trees.append((r, c))

    column_constraints = list(map(int, input().split()))

    N = 6  # board size

    # -----------------------------------------------------
    # --- Variables and domains ----------------------------

    variables = []

    for i in range(M):
        var = f"T{i}"
        variables.append(var)

        r, c = trees[i]

        domain = []

        # up
        if r - 1 >= 0 and (r - 1, c) not in trees:
            domain.append((r - 1, c))
        # down
        if r + 1 < N and (r + 1, c) not in trees:
            domain.append((r + 1, c))
        # left
        if c - 1 >= 0 and (r, c - 1) not in trees:
            domain.append((r, c - 1))
        # right
        if c + 1 < N and (r, c + 1) not in trees:
            domain.append((r, c + 1))

        problem.addVariable(var, domain)

    # -----------------------------------------------------
    # --- Constraints -------------------------------------

    # 1. All tents must be on different positions
    problem.addConstraint(AllDifferentConstraint(), variables)

    # 2. Column constraints
    for col in range(N):
        problem.addConstraint(
            count_in_col_i(col, column_constraints[col], variables),
            variables
        )

    # -----------------------------------------------------
    # --- Find solution -----------------------------------

    solution = problem.getSolution()

    # -----------------------------------------------------
    # --- Print tent positions -----------------------------

    if solution:
        tents = list(solution.values())
        for t in tents:
            print(t[1], t[0])
from constraint import Problem, BacktrackingSolver, MaxSumConstraint, ExactSumConstraint
from collections import defaultdict

if __name__ == '__main__':
    K = int(input())
    grid = [list(map(int, input().split())) for _ in range(K)]
    N = max(map(max, grid))

    problem = Problem(solver=BacktrackingSolver())

    # Add variables for regular stars
    for r in range(K):
        for c in range(K):
            problem.addVariable(('star', r, c), [0, 1])

    # Add variables for super stars (2x2 blocks)
    # A super star is defined by its top-left corner position
    for r in range(K - 1):
        for c in range(K - 1):
            problem.addVariable(('super', r, c), [0, 1])

    # Identify stable and unstable super star positions
    stable_supers = []
    unstable_supers = []

    for r in range(K - 1):
        for c in range(K - 1):
            # Check if all 4 cells of the 2x2 block are in the same region
            region_tl = grid[r][c]
            region_tr = grid[r][c + 1]
            region_bl = grid[r + 1][c]
            region_br = grid[r + 1][c + 1]

            if region_tl == region_tr == region_bl == region_br:
                stable_supers.append((r, c))
            else:
                unstable_supers.append((r, c))

    region_cells = defaultdict(list)
    for r in range(K):
        for c in range(K):
            region_cells[grid[r][c]].append((r, c))

    # Each region has at most 2 stars (counting regular stars and super stars)
    for region, cells in region_cells.items():
        region_vars = [('star', r, c) for r, c in cells]
        problem.addConstraint(MaxSumConstraint(2), region_vars)

    # TOTAL stars must equal N (counting super stars as 4 regular stars)
    all_star_vars = [('star', r, c) for r in range(K) for c in range(K)]
    problem.addConstraint(ExactSumConstraint(N), all_star_vars)

    # A cell can't be both a regular star and part of a super star
    for r in range(K - 1):
        for c in range(K - 1):
            # If super star at (r,c) is active, then the 4 cells must all be stars
            def super_star_constraint(super_val, tl, tr, bl, br):
                if super_val == 1:
                    return tl == 1 and tr == 1 and bl == 1 and br == 1
                return True


            problem.addConstraint(
                super_star_constraint,
                [('super', r, c), ('star', r, c), ('star', r, c + 1),
                 ('star', r + 1, c), ('star', r + 1, c + 1)]
            )

    # Different-region stars cannot share a row
    for r in range(K):
        for c1 in range(K):
            for c2 in range(c1 + 1, K):
                if grid[r][c1] != grid[r][c2]:
                    problem.addConstraint(MaxSumConstraint(1), [('star', r, c1), ('star', r, c2)])

    # Different-region stars cannot share a column
    for c in range(K):
        for r1 in range(K):
            for r2 in range(r1 + 1, K):
                if grid[r1][c] != grid[r2][c]:
                    problem.addConstraint(MaxSumConstraint(1), [('star', r1, c), ('star', r2, c)])

    # Same-region stars must not be orthogonally adjacent (unless part of a super star)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(K):
        for c in range(K):
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < K and 0 <= nc < K:
                    if grid[r][c] == grid[nr][nc]:
                        # They can only both be 1 if they're part of a super star
                        def adjacent_constraint(star1, star2, *super_vals):
                            if star1 == 1 and star2 == 1:
                                # Check if any super star covers both cells
                                return any(sv == 1 for sv in super_vals)
                            return True


                        # Find all super stars that could cover both (r,c) and (nr,nc)
                        covering_supers = []
                        for sr in range(max(0, min(r, nr) - 1), min(K - 1, max(r, nr) + 1)):
                            for sc in range(max(0, min(c, nc) - 1), min(K - 1, max(c, nc) + 1)):
                                # Check if super star at (sr, sc) covers both cells
                                cells_in_super = [(sr, sc), (sr, sc + 1), (sr + 1, sc), (sr + 1, sc + 1)]
                                if (r, c) in cells_in_super and (nr, nc) in cells_in_super:
                                    covering_supers.append(('super', sr, sc))

                        if covering_supers:
                            problem.addConstraint(
                                adjacent_constraint,
                                [('star', r, c), ('star', nr, nc)] + covering_supers
                            )
                        else:
                            problem.addConstraint(MaxSumConstraint(1), [('star', r, c), ('star', nr, nc)])

    # NEW CONSTRAINT: Regular stars cannot be adjacent to unstable super stars
    for ur, uc in unstable_supers:
        # Get all cells adjacent to the 2x2 block
        adjacent_to_unstable = set()
        for r in range(ur, ur + 2):
            for c in range(uc, uc + 2):
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < K and 0 <= nc < K:
                        # Only add if it's not part of the super star itself
                        if not (ur <= nr < ur + 2 and uc <= nc < uc + 2):
                            adjacent_to_unstable.add((nr, nc))

        # If unstable super star is active, adjacent cells can't be regular stars
        for ar, ac in adjacent_to_unstable:
            def unstable_adjacent_constraint(super_val, star_val):
                if super_val == 1:
                    return star_val == 0
                return True


            problem.addConstraint(
                unstable_adjacent_constraint,
                [('super', ur, uc), ('star', ar, ac)]
            )

    result = problem.getSolution()

    if result is None:
        print("No solution")
    else:
        for r in range(K):
            row_out = []
            for c in range(K):
                if result[('star', r, c)] == 1:
                    row_out.append('*')
                else:
                    row_out.append(str(grid[r][c]))
            print(' '.join(row_out))
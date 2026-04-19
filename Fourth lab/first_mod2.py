from constraint import Problem, BacktrackingSolver, MaxSumConstraint, ExactSumConstraint
from collections import defaultdict


def cells_between(pos1, pos2):
    """Return all cells between pos1 and pos2 (exclusive) if they're in same row/col"""
    r1, c1 = pos1
    r2, c2 = pos2

    cells = []

    # Same row
    if r1 == r2:
        min_c, max_c = min(c1, c2), max(c1, c2)
        for c in range(min_c + 1, max_c):
            cells.append((r1, c))
    # Same column
    elif c1 == c2:
        min_r, max_r = min(r1, r2), max(r1, r2)
        for r in range(min_r + 1, max_r):
            cells.append((r, c1))

    return cells


def has_black_hole_between(pos1, pos2, black_holes):
    """Check if there's a black hole between two positions"""
    between = cells_between(pos1, pos2)
    return any(cell in black_holes for cell in between)


def no_conflict_constraint(val1, val2, region1, region2, pos1, pos2, black_holes):
    """
    Two stars (val1=1, val2=1) from different regions can be in same row/col
    only if there's a black hole between them.
    """
    # If both cells have stars
    if val1 == 1 and val2 == 1:
        # If from different regions
        if region1 != region2:
            # They're in same row or column
            r1, c1 = pos1
            r2, c2 = pos2
            if r1 == r2 or c1 == c2:
                # Check if there's a black hole between them
                if not has_black_hole_between(pos1, pos2, black_holes):
                    return False
    return True


if __name__ == '__main__':
    K = int(input())
    grid = [list(map(int, input().split())) for _ in range(K)]
    N = max(map(max, grid))

    number_bh = int(input())
    black_holes = set()
    for i in range(number_bh):
        temp = tuple(map(int, input().split()))
        black_holes.add(temp)

    problem = Problem(solver=BacktrackingSolver())

    # Variables: each cell can have 0 (no star) or 1 (star)
    for r in range(K):
        for c in range(K):
            # Black holes cannot have stars
            if (r, c) in black_holes:
                problem.addVariable((r, c), [0])
            else:
                problem.addVariable((r, c), [0, 1])

    # Group cells by region
    region_cells = defaultdict(list)
    for r in range(K):
        for c in range(K):
            region_cells[grid[r][c]].append((r, c))

    # Constraint 1 & 2: Each region has at most 2 stars, total N stars
    for region, cells in region_cells.items():
        problem.addConstraint(MaxSumConstraint(2), cells)

    # Total stars must equal N
    all_cells = [(r, c) for r in range(K) for c in range(K)]
    problem.addConstraint(ExactSumConstraint(N), all_cells)

    # Constraint 3: Different-region stars cannot share row/column (unless black hole between)
    for r in range(K):
        for c1 in range(K):
            for c2 in range(c1 + 1, K):
                if grid[r][c1] != grid[r][c2]:
                    pos1, pos2 = (r, c1), (r, c2)
                    problem.addConstraint(
                        lambda v1, v2, r1=grid[r][c1], r2=grid[r][c2], p1=pos1, p2=pos2, bh=black_holes:
                        no_conflict_constraint(v1, v2, r1, r2, p1, p2, bh),
                        [pos1, pos2]
                    )

    for c in range(K):
        for r1 in range(K):
            for r2 in range(r1 + 1, K):
                if grid[r1][c] != grid[r2][c]:
                    pos1, pos2 = (r1, c), (r2, c)
                    problem.addConstraint(
                        lambda v1, v2, r1=grid[r1][c], r2=grid[r2][c], p1=pos1, p2=pos2, bh=black_holes:
                        no_conflict_constraint(v1, v2, r1, r2, p1, p2, bh),
                        [pos1, pos2]
                    )

    # Constraint 4: Same-region stars must not be orthogonally adjacent
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(K):
        for c in range(K):
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < K and 0 <= nc < K:
                    if grid[r][c] == grid[nr][nc]:
                        problem.addConstraint(MaxSumConstraint(1), [(r, c), (nr, nc)])

    # Solve
    result = problem.getSolution()

    if result is None:
        print("No Solution!")
    else:
        for r in range(K):
            row_out = []
            for c in range(K):
                if (r, c) in black_holes:
                    row_out.append("@")
                elif result[(r, c)] == 1:
                    row_out.append('*')
                else:
                    row_out.append(str(grid[r][c]))
            print(' '.join(row_out))
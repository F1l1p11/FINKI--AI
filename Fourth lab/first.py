from constraint import Problem, BacktrackingSolver, MaxSumConstraint, ExactSumConstraint
from collections import defaultdict

if __name__ == '__main__':
    K = int(input())
    grid = [list(map(int, input().split())) for _ in range(K)]
    N = max(map(max, grid))

    problem = Problem(solver=BacktrackingSolver())

    for r in range(K):
        for c in range(K):
            problem.addVariable((r, c), [0, 1])

    region_cells = defaultdict(list)
    for r in range(K):
        for c in range(K):
            region_cells[grid[r][c]].append((r, c))

    # Each region has at most 2 stars
    for region, cells in region_cells.items():
        problem.addConstraint(MaxSumConstraint(2), cells)

    # TOTAL stars must equal N
    all_cells = [(r, c) for r in range(K) for c in range(K)]
    problem.addConstraint(ExactSumConstraint(N), all_cells)

    # Different-region stars cannot share a row
    for r in range(K):
        for c1 in range(K):
            for c2 in range(c1 + 1, K):
                if grid[r][c1] != grid[r][c2]:
                    problem.addConstraint(MaxSumConstraint(1), [(r, c1), (r, c2)])

    # Different-region stars cannot share a column
    for c in range(K):
        for r1 in range(K):
            for r2 in range(r1 + 1, K):
                if grid[r1][c] != grid[r2][c]:
                    problem.addConstraint(MaxSumConstraint(1), [(r1, c), (r2, c)])

    # Same-region stars must not be orthogonally adjacent
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(K):
        for c in range(K):
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < K and 0 <= nc < K:
                    if grid[r][c] == grid[nr][nc]:
                        problem.addConstraint(MaxSumConstraint(1), [(r, c), (nr, nc)])

    result = problem.getSolution()

    if result is None:
        print("No solution")
    else:
        for r in range(K):
            row_out = []
            for c in range(K):
                if result[(r, c)] == 1:
                    row_out.append('*')
                else:
                    row_out.append(str(grid[r][c]))
            print(' '.join(row_out))
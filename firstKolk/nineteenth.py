from constraint import *

def same_row_col (q1,q2):
    x1,y1 = q1
    x2,y2 = q2
    return x1 != x2 and y1 != y2
def same_diagonal (q1,q2):
    x1,y1 = q1
    x2,y2 = q2
    return abs(x1-x2) != abs(y1-y2)

def solve_n_queens(n):
    problem = Problem(BacktrackingSolver())

    queens = []
    for q in range (1, n+1):
        queens.append(q)

    positions = []
    for i in range (n):
        for j in range (n):
            positions.append((i,j))

    for queen in queens:
        problem.addVariable(queen, positions)


    for q1 in queens:
        for q2 in queens:
            if q1 < q2:
                problem.addConstraint(lambda pos1,pos2: same_row_col(pos1,pos2),(q1,q2))

    for q1 in queens:
        for q2 in queens:
            if q1 < q2:
                problem.addConstraint(lambda pos1,pos2: same_diagonal(pos1,pos2),(q1,q2))

    if n <= 6:
        solutions = problem.getSolutions()
        return len(solutions)
    else:
        solution = problem.getSolution()
        return solution

if __name__ == '__main__':
    n = int(input())
    result = solve_n_queens(n)
    print(result)
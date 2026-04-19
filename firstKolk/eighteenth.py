from constraint import *

if __name__ == '__main__':
    solver = input()
    problem = Problem(BacktrackingSolver())
    if solver == "BacktrackingSolver":
        problem = Problem(BacktrackingSolver())
    if solver == "RecursiveBacktrackingSolver":
        problem = Problem(RecursiveBacktrackingSolver())
    if solver == "MinConflictsSolver":
        problem = Problem(MinConflictsSolver())

    for i in range(9):
        for j in range(9):
            problem.addVariable((i,j),range(1,10))

    #row constraint
    for i in range(9):
        row = []
        for j in range(9):
            row.append((i,j))
        problem.addConstraint(AllDifferentConstraint(),row)

    #col constraint
    for i in range(9):
        col = []
        for j in range(9):
            col.append((j,i))
        problem.addConstraint(AllDifferentConstraint(), col)
    #block constraint
    for i in [0,3,6]:
        for j in [0,3,6]:
            block = []
            for k in range(3):
                for l in range(3):
                    block.append((i+k,j+l))
            problem.addConstraint(AllDifferentConstraint(),block)

    # Print only the first solution
    solution = problem.getSolution()

    if solution:
        print("{", end="")
        for i in range(9):
            for j in range(9):
                idx = i*9 + j
                if idx != 80:
                    print(f"{idx}: {solution[(i, j)]}", end=", ")
                else:
                    print(f"{idx}: {solution[(i, j)]}", end="")
        print("}")
    else:
        print("None")
from constraint import *

if __name__ == '__main__':
    problem = Problem(BacktrackingSolver())
    variables = ["S", "E", "N", "D", "M", "O", "R", "Y"]
    for variable in variables:
        problem.addVariable(variable, Domain(set(range(10))))

    problem.addConstraint(AllDifferentConstraint(), variables)

    # The main equation: SEND + MORE = MONEY
    # SEND = 1000*S + 100*E + 10*N + D
    # MORE = 1000*M + 100*O + 10*R + E
    # MONEY = 10000*M + 1000*O + 100*N + 10*E + Y
    problem.addConstraint(
        lambda S, E, N, D, M, O, R, Y:
        (1000 * S + 100 * E + 10 * N + D) + (1000 * M + 100 * O + 10 * R + E) ==
        (10000 * M + 1000 * O + 100 * N + 10 * E + Y),
        variables
    )

    print(problem.getSolution())
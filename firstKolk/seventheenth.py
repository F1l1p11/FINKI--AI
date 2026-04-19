from constraint import *

if __name__ == '__main__':
    problem = Problem(BacktrackingSolver())
    variables = ["A", "B", "C", "D", "E", "F"]
    for variable in variables:
        problem.addVariable(variable, Domain(set(range(100))))

    problem.addConstraint(MinSumConstraint(100),["A", "B", "C"])
    problem.addConstraint(lambda B: B % 2 == 1, ["B"])
    problem.addConstraint(lambda D: D % 2 == 1, ["D"])
    problem.addConstraint(lambda E: E % 2 == 1, ["E"])
    problem.addConstraint(ExactSumConstraint(150),["D","E"])
    problem.addConstraint(lambda F: (F % 10) % 4 == 0, ["F"])
    problem.addConstraint(AllDifferentConstraint(), variables)

    print(problem.getSolution())

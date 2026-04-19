from constraint import *

if __name__ == '__main__':
    num = int(input())

    papers = dict()

    paper_info = input()
    while paper_info != 'end':
        title, topic = paper_info.split(' ')
        papers[title] = topic
        paper_info = input()

    # Define the variables - each paper is a variable
    variables = list(papers.keys())

    domain = [f'T{i + 1}' for i in range(num)]

    problem = Problem(BacktrackingSolver())

    # Change this section if necessary
    problem.addVariables(variables, domain)

    # Add the constraints

    # Constraint 1: At most 4 papers can be presented in each time slot
    for time_slot in domain:
        def max_4_per_slot(*assignments, slot=time_slot):
            count = sum(1 for assignment in assignments if assignment == slot)
            return count <= 4


        problem.addConstraint(max_4_per_slot, variables)

    # Constraint 2: If the number of papers from a given area is <= max papers per slot (4),
    # then those papers should be assigned to the same slot
    topic_groups = {}
    for paper, topic in papers.items():
        if topic not in topic_groups:
            topic_groups[topic] = []
        topic_groups[topic].append(paper)

    for topic, topic_papers in topic_groups.items():
        if len(topic_papers) <= 4:
            # All papers from this topic should be in the same slot
            if len(topic_papers) > 1:
                problem.addConstraint(
                    AllEqualConstraint(),
                    topic_papers
                )

    result = problem.getSolution()

    # Add the required print section
    if result:
        for paper in variables:
            print(f"{paper} ({papers[paper]}): {result[paper]}")
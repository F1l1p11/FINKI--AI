from searching_frameworks import Problem, breadth_first_graph_search

class Hanoi(Problem):
    def __init__(self, initial, goal):
        super().__init__(initial)
        self.goal = goal

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]

    def goal_test(self, state):
        return state == self.goal

    def successor(self, state):
        successor = {}
        n = len(state)

        for i in range(n):
            if len(state[i]) == 0:
                continue

            for j in range(n):
                if i == j:
                    continue

                if len(state[j]) == 0 or state[i][-1] <= state[j][-1]:
                    new_state = [list(p) for p in state]

                    disk = new_state[i].pop()
                    new_state[j].append(disk)

                    new_state = tuple(tuple(p) for p in new_state)

                    action = f"MOVE TOP BLOCK FROM PILLAR {i+1} TO PILLAR {j+1}"
                    successor[action] = new_state

        return successor


if __name__ == '__main__':
    initial_input = input().split(';')
    goal_input = input().split(';')

    def parse(line):
        pillars = []
        for part in line:
            if part == '':
                pillars.append(tuple())
            else:
                pillars.append(tuple(map(int, part.split(','))))
        return tuple(pillars)

    initial = parse(initial_input)
    goal = parse(goal_input)

    problem = Hanoi(initial, goal)
    result = breadth_first_graph_search(problem)

    if result:
        print("Number of action", len(result.solution()))
        print(result.solution())
    else:
        print("No Solution!")
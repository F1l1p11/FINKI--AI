from searching_frameworks import Problem, breadth_first_graph_search

dir = {"up": (0, +1), "down": (0, -1), "left": (-1, 0), "right": (+1, 0)}

class Robot(Problem):
    def __init__(self, initial):
        super().__init__(initial)
        self.goal = ((0,4),(1,3),(2,2),(3,1),(4,0))

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]

    def goal_test(self, state):
        return state == self.goal

    def in_bounds(self, x, y):
        return 0 <= x < 5 and 0 <= y < 5

    def successor(self, state):
        successor = {}

        for i in range(5):
            x, y = state[i]

            for d in dir:
                dx, dy = dir[d]
                nx, ny = x + dx, y + dy

                if self.in_bounds(nx, ny):
                    new_tup = list(state)
                    new_tup[i] = (nx, ny)
                    new_tup = tuple(new_tup)

                    action = "Move square " + str(i+1) + " " + d
                    successor[action] = new_tup

        return successor


if __name__ == '__main__':
    initial_pos = []
    for _ in range(5):
        temp = tuple(map(int, input().split(",")))
        initial_pos.append(temp)

    initial = tuple(initial_pos)

    problem = Robot(initial)
    result = breadth_first_graph_search(problem)

    if result is not None:
        print(result.solution())
    else:
        print("No Solution!")
from searching_frameworks import Problem, breadth_first_graph_search

class LightsOut(Problem):
    def __init__(self, initial, n):
        super().__init__(initial)
        self.n = n

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]

    def goal_test(self, state):
        for row in state:
            for cell in row:
                if cell != 1:
                    return False
        return True

    def successor(self, state):
        successor = {}

        for i in range(self.n):
            for j in range(self.n):

                # copy state
                new_state = [list(row) for row in state]

                # helper to toggle
                def toggle(x, y):
                    if 0 <= x < self.n and 0 <= y < self.n:
                        new_state[x][y] = 1 - new_state[x][y]

                # toggle center + neighbors
                toggle(i, j)
                toggle(i-1, j)
                toggle(i+1, j)
                toggle(i, j-1)
                toggle(i, j+1)

                # convert back to tuple
                new_state_tuple = tuple(tuple(row) for row in new_state)

                action = f"x: {i}, y: {j}"
                successor[action] = new_state_tuple

        return successor

if __name__ == '__main__':
    n = int(input())
    fields = list(map(int, input().split(',')))

    # convert to matrix
    matrix = []
    idx = 0
    for i in range(n):
        row = []
        for j in range(n):
            row.append(fields[idx])
            idx += 1
        matrix.append(tuple(row))

    initial = tuple(matrix)

    problem = LightsOut(initial, n)
    result = breadth_first_graph_search(problem)

    if result:
        print(result.solution())
    else:
        print("No solution!")
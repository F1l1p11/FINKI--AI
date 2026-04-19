from searching_framework import Problem, astar_search

class Maze(Problem):
    def __init__(self, initial, goal, n, walls):
        super().__init__(initial, goal)
        self.n = n
        self.walls = set(walls)

    def valid(self, x, y):
        return 0 <= x < self.n and 0 <= y < self.n and (x, y) not in self.walls

    def successor(self, state):
        successors = {}
        x, y = state

        if self.valid(x, y + 1):
            successors["Gore"] = (x, y + 1)

        if self.valid(x, y - 1):
            successors["Dolu"] = (x, y - 1)

        if self.valid(x - 1, y):
            successors["Levo"] = (x - 1, y)

        if self.valid(x + 1, y) and self.valid(x + 2, y) and self.valid(x + 3, y):
            successors["Desno 3"] = (x + 3, y)
        elif self.valid(x + 1, y) and self.valid(x + 2, y):
            successors["Desno 2"] = (x + 2, y)

        return successors

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]

    def h(self, node):
        x, y = node.state
        gx, gy = self.goal

        dx = abs(x - gx)
        dy = abs(y - gy)

        return (dx // 3 + dx % 3) + dy


if __name__ == '__main__':
    n = int(input())

    num_walls = int(input())
    walls = []

    for _ in range(num_walls):
        x, y = map(int, input().split(","))
        walls.append((x, y))

    start = tuple(map(int, input().split(",")))
    goal = tuple(map(int, input().split(",")))

    problem = Maze(start, goal, n, walls)

    result = astar_search(problem)
    if result is None:
        print("No Solution!")
    else:
        print(result.solution())
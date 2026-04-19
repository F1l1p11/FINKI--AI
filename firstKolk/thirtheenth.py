from searching_frameworks import Problem, breadth_first_graph_search, astar_search

class Squares(Problem):
    def __init__(self, initial,size,walls,man):
        super().__init__(initial)
        self.size = size
        self.walls = walls
        self.man = man

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]

    def goal_test(self, state):
        ghost = state
        return ghost == self.man

    def h(self, node):
        ghost = node.state
        gx, gy = ghost
        mx, my = self.goal

        return abs(gx - mx) / 3 + abs(gy - my) / 3

    def successor(self, state):
        successor = {}
        # up right
        ghost = state
        gx, gy = ghost

        # up
        if 0 <= gx < self.size and 0 <= gy + 3 < self.size and (gx, gy + 3) not in self.walls:
            successor["Up 3"] = (gx, gy + 3)

        if 0 <= gx < self.size and 0 <= gy + 2 < self.size and (gx, gy + 2) not in self.walls:
            successor["Up 2"] = (gx, gy + 2)

        if 0 <= gx < self.size and 0 <= gy + 1 < self.size and (gx, gy + 1) not in self.walls:
            successor["Up 1"] = (gx, gy + 1)

        # right
        if 0 <= gx + 3 < self.size and 0 <= gy < self.size and (gx + 3, gy) not in self.walls:
            successor["Right 3"] = (gx + 3, gy)

        if 0 <= gx + 2 < self.size and 0 <= gy < self.size and (gx + 2, gy) not in self.walls:
            successor["Right 2"] = (gx + 2, gy)

        if 0 <= gx + 1 < self.size and 0 <= gy < self.size and (gx + 1, gy) not in self.walls:
            successor["Right 1"] = (gx + 1, gy)

        return successor


if __name__ == '__main__':
    size = int(input())
    number_walls = int(input())
    walls = []
    for i in range(number_walls):
        temp = tuple(map(int, input().split(",")))
        walls.append(temp)
    walls = tuple(walls)

    ghost = tuple((0,0))
    man = (size-1,size-1)

    initial = ghost

    problem = Squares(initial,size,walls,man)
    result = astar_search(problem)

    if result is not None:
        print(result.solution())
    else:
        print("No Solution!")
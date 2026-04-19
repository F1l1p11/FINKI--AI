from searching_frameworks import Problem, astar_search, breadth_first_graph_search


class HouseProblem(Problem):
    def __init__(self, initial, allowed, width, height):
        super().__init__(initial)
        self.allowed = allowed
        self.width = width
        self.height = height

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]

    def goal_test(self, state):
        person, house, direction = state
        return person == house

    def move_house(self, house, dir):
        hx, hy = house
        if 0 <= hx + dir < self.width:
            return hx + dir, hy, dir
        else:
            new_dir = -dir
            return hx + new_dir, hy, new_dir

    def successor(self, state):
        successor = {}
        person, house, direction = state
        px, py = person
        dir = direction

        # Calculate where the house will be after this move
        nx, ny, nd = self.move_house(house, dir)

        # Wait - allowed if on allowed cell OR already at the house
        if (px, py) in self.allowed or (px, py) == house:
            successor["Wait"] = ((px, py), (nx, ny), nd)

        # Up 1
        new_pos = (px, py + 1)
        if 0 <= py + 1 < self.height:
            # Can land here if it's an allowed cell OR if we're landing on the house in top row
            if new_pos in self.allowed or (py + 1 == self.height - 1 and new_pos == (nx, ny)):
                successor["Up 1"] = (new_pos, (nx, ny), nd)

        # Up 2
        new_pos = (px, py + 2)
        if 0 <= py + 2 < self.height:
            if new_pos in self.allowed or (py + 2 == self.height - 1 and new_pos == (nx, ny)):
                successor["Up 2"] = (new_pos, (nx, ny), nd)

        # Up-right 1
        new_pos = (px + 1, py + 1)
        if 0 <= px + 1 < self.width and 0 <= py + 1 < self.height:
            if new_pos in self.allowed or (py + 1 == self.height - 1 and new_pos == (nx, ny)):
                successor["Up-right 1"] = (new_pos, (nx, ny), nd)

        # Up-right 2
        new_pos = (px + 2, py + 2)
        if 0 <= px + 2 < self.width and 0 <= py + 2 < self.height:
            if new_pos in self.allowed or (py + 2 == self.height - 1 and new_pos == (nx, ny)):
                successor["Up-right 2"] = (new_pos, (nx, ny), nd)

        # Up-left 1
        new_pos = (px - 1, py + 1)
        if 0 <= px - 1 < self.width and 0 <= py + 1 < self.height:
            if new_pos in self.allowed or (py + 1 == self.height - 1 and new_pos == (nx, ny)):
                successor["Up-left 1"] = (new_pos, (nx, ny), nd)

        # Up-left 2
        new_pos = (px - 2, py + 2)
        if 0 <= px - 2 < self.width and 0 <= py + 2 < self.height:
            if new_pos in self.allowed or (py + 2 == self.height - 1 and new_pos == (nx, ny)):
                successor["Up-left 2"] = (new_pos, (nx, ny), nd)

        return successor

    def h(self, node):
        person, house, direction = node.state
        px, py = person
        hx, hy = house
        return max(abs(px - hx), abs(py - hy)) // 2


if __name__ == '__main__':
    allowed = [(1, 0), (2, 0), (3, 0), (1, 1), (2, 1), (0, 2), (2, 2), (4, 2), (1, 3), (3, 3), (4, 3), (0, 4), (2, 4),
               (2, 5), (3, 5), (0, 6), (2, 6), (1, 7), (3, 7)]
    width = 5
    height = 9
    person = tuple(map(int, input().split(",")))
    house = tuple(map(int, input().split(",")))
    direction = input()
    if direction == "right":
        direction = +1
    else:
        direction = -1
    initial = (person, house, direction)
    problem = HouseProblem(initial, allowed, width, height)
    result = astar_search(problem)

    if result:
        print(result.solution())
    else:
        print("No solution!")
from searching_framework import Problem, breadth_first_graph_search

directions = {"up": (0, 1),"down": (0, -1),"right": (1, 0),"up-right": (1, 1),"down-right": (1, -1)}

class Football(Problem):
    def __init__(self, initial):
        super().__init__(initial)
        self.width = 8
        self.height = 6
        self.goals = [(7, 2), (7, 3)]

    def goal_test(self, state):
        _, _, x, y, _, _ = state
        return (x, y) in self.goals

    def valid(self, man, ball, o1, o2):
        mx, my = man
        bx, by = ball

        if not (0 <= mx < self.width and 0 <= my < self.height):
            return False
        if not (0 <= bx < self.width and 0 <= by < self.height):
            return False

        if man == ball:
            return False

        if man == o1 or man == o2:
            return False
        if ball == o1 or ball == o2:
            return False

        # ball cannot be near opponents
        for (ox, oy) in [o1, o2]:
            for x in [-1, 0, 1]:
                for y in [-1, 0, 1]:
                    if (bx, by) == (ox + x, oy + y):
                        return False

        return True

    def move_opponents(self, o1, o2):
        # toggle positions
        if o1 == (3, 3):
            new_o1 = (3, 4)
        else:
            new_o1 = (3, 3)

        if o2 == (5, 4):
            new_o2 = (5, 3)
        else:
            new_o2 = (5, 4)

        return new_o1, new_o2

    def successor(self, state):
        mx, my, bx, by, o1, o2 = state
        successors = {}

        for d in directions:
            dx, dy = directions[d]
            new_mx = mx + dx
            new_my = my + dy

            # move opponents AFTER player move
            next_o1, next_o2 = self.move_opponents(o1, o2)

            if (new_mx, new_my) == (bx, by):
                new_bx = bx + dx
                new_by = by + dy

                if self.valid((new_mx, new_my), (new_bx, new_by), next_o1, next_o2):
                    successors[f"Push ball {d}"] = (
                        new_mx, new_my, new_bx, new_by, next_o1, next_o2
                    )
            else:
                if self.valid((new_mx, new_my), (bx, by), next_o1, next_o2):
                    successors[f"Move man {d}"] = (new_mx, new_my, bx, by, next_o1, next_o2)

        return successors

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]


if __name__ == '__main__':
    man = tuple(map(int,input().split(',')))
    ball = tuple(map(int,input().split(',')))
    o1 = (3, 3)
    o2 = (5, 4)

    initial = (man[0], man[1], ball[0], ball[1], o1, o2)
    problem = Football(initial)
    result = breadth_first_graph_search(problem)
    if result is not None:
        print(result.solution())
    else:
        print("No Solution!")
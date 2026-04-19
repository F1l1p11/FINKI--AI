from searching_framework import Problem, breadth_first_graph_search

directions = {"up": (0, 1),"down": (0, -1),"right": (1, 0),"up-right": (1, 1),"down-right": (1, -1)}

class Football(Problem):
    def __init__(self, initial):
        super().__init__(initial)
        self.width = 8
        self.height = 6
        self.initial_opponents = [(3, 3), (5, 4)]
        self.initial_dirs = (1, -1)  # 1 = moving up, -1 = moving down
        self.goals = [(7, 2), (7, 3)]

    def goal_test(self, state):
        _, _, bx, by, _, _ = state
        return (bx, by) in self.goals

    def valid(self, man, ball, opponents):
        mx, my = man
        bx, by = ball
        if not (0 <= mx < self.width and 0 <= my < self.height):
            return False
        if not (0 <= bx < self.width and 0 <= by < self.height):
            return False
        if man == ball:
            return False
        if man in opponents:
            return False
        if ball in opponents:
            return False
        for ox, oy in opponents:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if (bx, by) == (ox+dx, oy+dy):
                        return False
        return True

    def move_opponents(self, opponents, dirs):
        new_opponents = []
        new_dirs = []
        for (x, y), d in zip(opponents, dirs):
            ny = y + d
            if ny < 0:
                ny = 0
                d = 1
            elif ny >= self.height:
                ny = self.height - 1
                d = -1
            new_opponents.append((x, ny))
            new_dirs.append(d)
        return tuple(new_opponents), tuple(new_dirs)

    def successor(self, state):
        mx, my, bx, by, opponents, dirs = state
        # move opponents first
        opponents, dirs = self.move_opponents(opponents, dirs)

        successors = {}
        for d in directions:
            dx, dy = directions[d]
            new_mx = mx + dx
            new_my = my + dy
            if (new_mx, new_my) == (bx, by):
                new_bx = bx + dx
                new_by = by + dy
                if self.valid((new_mx, new_my), (new_bx, new_by), opponents):
                    successors[f"Push ball {d}"] = (new_mx, new_my, new_bx, new_by, opponents, dirs)
            else:
                if self.valid((new_mx, new_my), (bx, by), opponents):
                    successors[f"Move man {d}"] = (new_mx, new_my, bx, by, opponents, dirs)
        return successors

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]

if __name__ == '__main__':
    man = tuple(map(int,input().split(',')))
    ball = tuple(map(int,input().split(',')))
    # initial state: man_x, man_y, ball_x, ball_y, opponents, opponent_dirs
    initial = (man[0], man[1], ball[0], ball[1], ((3,3),(5,4)), (1,-1))
    problem = Football(initial)
    result = breadth_first_graph_search(problem)
    if result is not None:
        print(result.solution())
    else:
        print("No Solution!")
from searching_framework import Problem, breadth_first_graph_search

directions = {"up": (0, 1),"down": (0, -1),"right": (1, 0),"up-right": (1, 1),"down-right": (1, -1)}

class Football(Problem):
    def __init__(self,initial):
        super().__init__(initial)
        self.width = 8
        self.height = 6
        self.opponents = [(3, 3), (5, 4)]
        self.goals = [(7, 2), (7, 3)]

    def goal_test(self, state):
        _,_,x,y = state
        return (x,y) in self.goals

    def valid (self,man,ball):
        mx,my = man
        bx,by = ball
        if not (0 <= mx < self.width and 0 <= my < self.height):
            return False

        if not (0 <= bx < self.width and 0 <= by < self.height):
            return False
        if man == ball:
            return False
        if man in self.opponents:
            return False
        if ball in self.opponents:
            return False
        for opponent in self.opponents:
            ox,oy = opponent
            for x in [-1,0,1]:
                for y in [-1,0,1]:
                    if (bx,by) == (ox+x,oy+y):
                        return False
        return True

    def successor(self,state):
        mx,my,bx,by = state
        successors = {}
        for d in directions:
            dx,dy = directions[d]
            new_mx = mx + dx
            new_my = my + dy
            if (new_mx, new_my) == (bx, by):
                new_bx = bx + dx
                new_by = by + dy
                if self.valid((new_mx, new_my), (new_bx, new_by)):
                    successors[f"Push ball {d}"] = (new_mx, new_my, new_bx, new_by)
            else:
                if self.valid((new_mx, new_my), (bx, by)):
                    successors[f"Move man {d}"] = (new_mx, new_my, bx, by)
        return successors

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]


if __name__ == '__main__':
    man = tuple(map(int,input().split(',')))
    ball = tuple(map(int,input().split(',')))
    initial = (man[0],man[1],ball[0],ball[1])
    problem = Football(initial)
    result = breadth_first_graph_search(problem)
    if result is not None:
        print(result.solution())
    else:
        print("No Solution!")
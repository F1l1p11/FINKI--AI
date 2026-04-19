from searching_frameworks  import Problem, breadth_first_graph_search

dir = {"up": (0, +1),"down": (0, -1),"right": (+1, 0),"up-right" : (+1,+1), "down-right" : (+1,-1)}

class Robot(Problem):
    def __init__(self, initial,width,height,opp_1,opp_2,goal):
        super().__init__(initial)
        self.width = width
        self.height = height
        self.opp_1 = opp_1
        self.opp_2 = opp_2
        self.goal = goal

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]

    def goal_test(self, state):
        _, ball = state
        return ball in self.goal

    def in_bounds(self, x,y):
        return 0 <= x < self.width and 0 <= y < self.height

    def ball_valid(self, x,y):
        for sx in [-1,0,1]:
            for sy in [-1,0,1]:
                o1x,o1y = self.opp_1
                o2x,o2y = self.opp_2
                if (o1x+sx,o1y+sy) == (x,y) or (o2x+sx,o2y+sy) == (x,y):
                    return False
        return True

    def successor(self, state):
        man,ball = state
        successor = {}
        for d in dir:
            mx,my = man
            bx,by = ball
            dx,dy = dir[d]
            nx,ny = mx+dx,my+dy
            if self.in_bounds(nx,ny) and (nx,ny) != opp_1 and (nx,ny) != opp_2:
                if (nx,ny) == (bx,by) and self.in_bounds(bx+dx,by+dy) and self.ball_valid(bx+dx,by+dy):
                    nbx,nby = bx + dx, by + dy
                    successor ["Push ball " + d] = ((nx,ny),(nbx,nby))
                elif (nx,ny) != (bx,by):
                    successor ["Move man " + d] = ((nx,ny),(bx,by))
        return successor


if __name__ == '__main__':
    width = 8
    height = 6
    opp_1 = (3,3)
    opp_2 = (5,4)
    goal = [(7,2),(7,3)]
    man = tuple(map(int,input().split(",")))
    ball = tuple(map(int,input().split(",")))
    initial = (man,ball)
    problem = Robot(initial,width,height,opp_1,opp_2,goal)
    result = breadth_first_graph_search(problem)
    if result is not None:
        print(result.solution())
    else:
        print("No Solution!")
from searching_frameworks import Problem, breadth_first_graph_search
#up-right, up-left, down-right, down-left, left, or right
dir = {"Up Right" : (+2,+2), "Up Left" : (-2,+2), "Down Right" : (+2,-2), "Down Left" : (-2,-2), "Left" : (-2, 0), "Right" : (+2, 0)}
dir_second = {"Up Right" : (+1,+1), "Up Left" : (-1,+1), "Down Right" : (+1,-1), "Down Left" : (-1,-1), "Left" : (-1, 0), "Right" : (+1, 0)}

class Robot(Problem):
    def __init__(self, initial,size,pos_walls):
        super().__init__(initial)
        self.size = size
        self.pos_walls = pos_walls

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]

    def goal_test(self, state):
        pos_balls = state
        bx,by = pos_balls[0]
        temp = (self.size//2)
        pos_balls = tuple(pos_balls)
        return (bx,by) == (temp,self.size-1) and len(pos_balls) == 1

    def in_bounds(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size

    def successor(self, state):
        successor = {}
        balls = state
        for d in dir:
            dx,dy = dir[d]
            ddx,ddy = dir_second[d]
            for bx, by in balls:
                nbx,nby = bx+ddx,by+ddy
                if (nbx,nby) in balls and self.in_bounds(nbx,nby) and (nbx,nby) not in self.pos_walls:
                    nnbx,nnby = bx+dx,by+dy
                    if self.in_bounds(nnbx,nnby) and (nnbx,nnby) not in balls and (nnbx,nnby) not in self.pos_walls:
                        temp_x,temp_y = bx,by
                        new_tup = list(balls)
                        new_tup.remove((bx,by))
                        new_tup.remove((nbx,nby))
                        new_tup.append((nnbx,nnby))
                        new_tup = tuple(new_tup)
                        successor[d + ": (x=" + str(temp_x) + ",y=" + str(temp_y) + ")"] = new_tup
        #return successor
        return dict(sorted(successor.items()))

if __name__ == '__main__':
    size = int(input())

    num_balls = int(input())
    pos_balls = []
    for i in range(num_balls):
        temp = tuple(map(int, input().split(",")))
        pos_balls.append(temp)
    pos_balls = tuple(pos_balls)

    num_walls = int(input())
    pos_walls = []
    for i in range(num_walls):
        temp = tuple(map(int, input().split(",")))
        pos_walls.append(temp)
    pos_walls = tuple(pos_walls)

    initial = pos_balls
    problem = Robot(initial,size,pos_walls)
    result = breadth_first_graph_search(problem)

    if result is not None:
        print(result.solution())
    else:
        print("No Solution!")
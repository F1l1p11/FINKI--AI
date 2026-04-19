from searching_frameworks  import Problem, breadth_first_graph_search

class Box(Problem):
    def __init__(self, initial, goal):
        super().__init__(initial)
        self.goal = goal

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]

    def goal_test(self, state):
        _, first_box, second_box = state
        fx,fy = first_box
        sx,sy = second_box
        return (fx,fy) == (4,4) and (sx,sy) == (4,4)

    dir = {"up" : (0,+1), "down" : (0,-1), "left" : (-1,0), "right" : (+1,0)}

    def smth (self,x,y):
        return 0 <= x <= 4 and 0 <= y <= 4

    def successor(self, state):
        succ = {}
        man, first_box, second_box = state
        mx, my = man
        fx, fy = first_box
        sx, sy = second_box
        #up,down,left,right
        for d in self.dir:
            dx,dy=self.dir[d]
            nx,ny = mx+dx,my+dy
            if self.smth(nx,ny) and (nx,ny) != (fx,fy) and (nx,ny) != (sx,sy):
                succ["Move man " + d] = ((nx,ny),(fx,fy),(sx,sy))
            if self.smth(nx,ny) and (nx,ny) == (fx,fy):
                nfx, nfy = fx+dx,fy+dy
                if self.smth(nfx,nfy) and (nfx,nfy) == (4,4):
                    succ["Push box 1 " + d] = ((nx,ny),(nfx, nfy),(sx,sy))
                elif (nfx,nfy) != (sx,sy):
                    succ["Push box 1 " + d] = ((nx, ny), (nfx, nfy), (sx, sy))
            if self.smth(nx,ny) and (nx,ny) == (sx,sy):
                nsx, nsy = sx+dx,sy+dy
                if self.smth(nsx,nsy) and (nsx,nsy) == (4,4):
                    succ["Push box 2 " + d] = ((nx,ny),(fx,fy),(nsx, nsy))
                elif (nsx,nsy) != (fx,fy):
                    succ["Push box 2 " + d] = ((nx, ny), (fx, fy), (nsx, nsy))

        return succ

if __name__ == '__main__':
    man = tuple(map(int, input().split(",")))
    first_box = tuple(map(int, input().split(",")))
    second_box = tuple(map(int, input().split(",")))
    initial = (man, first_box, second_box)
    problem = Box(initial,(4,4))
    result = breadth_first_graph_search(problem)
    if result is not None:
        print(result.solution())
    else:
        print("No Solution!")
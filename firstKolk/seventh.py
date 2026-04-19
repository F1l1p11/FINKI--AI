from searching_frameworks import Problem, breadth_first_graph_search

dir = {"Right": (+1, 0),"Up": (0, +1),"Left": (-1, 0),"Down": (0, -1)}

class Robot(Problem):
    def __init__(self, initial, m1_pos,m1_steps, m2_pos,m2_steps,m1_parts,m2_parts,walls):
        super().__init__(initial)
        self.m1_pos = m1_pos
        self.m1_steps = m1_steps
        self.m2_pos = m2_pos
        self.m2_steps = m2_steps
        self.m1_parts = m1_parts
        self.m2_parts = m2_parts
        self.walls = walls

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]

    def goal_test(self, state):
        _,_,_,_,tmp1,tmp2,_ = state
        return tmp1 and tmp2

    def successor(self, state):
        x, y, c1, c2, M1_fixed, M2_fixed, repair = state
        successor = {}
        for d in dir:
            dx,dy = dir[d]
            nx,ny = (x+dx,y+dy)
            if 0 <= nx < 10 and 0 <= ny < 10 and (nx,ny) not in self.walls:
                new_c1 = c1
                new_c2 = c2
                if (nx,ny) in self.m1_parts and (nx,ny) not in c1:
                    new_c1 = tuple(list(c1) + [(nx,ny)])
                if M1_fixed and (nx,ny) in self.m2_parts and (nx,ny) not in c2:
                    new_c2 = tuple(list(c2) + [(nx,ny)])
                successor[d] = (nx,ny,new_c1,new_c2,M1_fixed,M2_fixed,0)
        if (x,y) == self.m1_pos and not M1_fixed and len(c1) == len(self.m1_parts):
            if repair + 1 == self.m1_steps:
                successor["Repair"] = (x,y,c1,c2,True,M2_fixed,0)
            else:
                successor["Repair"] = (x,y,c1,c2,M1_fixed,M2_fixed,repair+1)
        elif (x,y) == self.m2_pos and M1_fixed and not M2_fixed and len(c2) == len(self.m2_parts):
            if repair + 1 == self.m2_steps:
                successor["Repair"] = (x,y,c1,c2,M1_fixed,True,0)
            else:
                successor["Repair"] = (x,y,c1,c2,M1_fixed,M2_fixed,repair+1)
        return successor


if __name__ == '__main__':
    robot_start_pos = tuple(map(int, input().split(',')))
    M1_pos = tuple(map(int, input().split(',')))
    M1_steps = int(input())
    M2_pos = tuple(map(int, input().split(',')))
    M2_steps = int(input())
    parts_M1 = int(input())
    to_collect_M1 = tuple([tuple(map(int, input().split(','))) for _ in range(parts_M1)])
    parts_M2 = int(input())
    to_collect_M2 = tuple([tuple(map(int, input().split(','))) for _ in range(parts_M2)])

    walls = [(4, 0), (5, 0), (7, 5), (8, 5), (9, 5), (1, 6), (1, 7), (0, 6), (0, 8), (0, 9), (1, 9), (2, 9), (3, 9)]
    initial = (robot_start_pos[0], robot_start_pos[1], (), (), False, False, 0)
    problem = Robot(initial, M1_pos, M1_steps, M2_pos, M2_steps,to_collect_M1, to_collect_M2, walls)
    result = breadth_first_graph_search(problem)
    if result is not None:
        print(result.solution())
    else:
        print("No Solution!")
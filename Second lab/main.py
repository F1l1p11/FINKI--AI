from searching_framework import *

dir = {"Up": (0,1), "Down": (0,-1), "Left": (-1,0), "Right": (1,0)}

class Robot(Problem):

    def __init__(self, initial, M1_pos, M1_steps, M2_pos, M2_steps,
                 parts1, parts2, walls):

        super().__init__(initial)
        self.M1_pos = M1_pos
        self.M2_pos = M2_pos
        self.M1_steps = M1_steps
        self.M2_steps = M2_steps
        self.parts1 = parts1
        self.parts2 = parts2
        self.walls = walls


    def goal_test(self, state):
        _,_,_,_,M1_fixed,M2_fixed,_ = state
        return M1_fixed and M2_fixed


    def successor(self, state):

        x,y,c1,c2,M1_fixed,M2_fixed,repair = state
        succ = {}

        # MOVEMENTS
        for d in dir:
            dx,dy = dir[d]
            nx,ny = x+dx,y+dy

            if 0<=nx<10 and 0<=ny<10 and (nx,ny) not in self.walls:

                new_c1 = c1
                new_c2 = c2

                # collect M1 parts
                if (nx,ny) in self.parts1 and (nx,ny) not in c1:
                    new_c1 = tuple(list(c1)+[(nx,ny)])

                # collect M2 parts (only if M1 fixed)
                if M1_fixed and (nx,ny) in self.parts2 and (nx,ny) not in c2:
                    new_c2 = tuple(list(c2)+[(nx,ny)])

                succ[d] = (nx,ny,new_c1,new_c2,M1_fixed,M2_fixed,0)


        # REPAIR
        if (x,y) == self.M1_pos and not M1_fixed and len(c1)==len(self.parts1):

            if repair+1 == self.M1_steps:
                succ["Repair"] = (x,y,c1,c2,True,M2_fixed,0)
            else:
                succ["Repair"] = (x,y,c1,c2,M1_fixed,M2_fixed,repair+1)


        elif (x,y) == self.M2_pos and M1_fixed and not M2_fixed and len(c2)==len(self.parts2):

            if repair+1 == self.M2_steps:
                succ["Repair"] = (x,y,c1,c2,M1_fixed,True,0)
            else:
                succ["Repair"] = (x,y,c1,c2,M1_fixed,M2_fixed,repair+1)


        return succ


    def actions(self, state):
        return self.successor(state).keys()


    def result(self, state, action):
        return self.successor(state)[action]
if __name__ == '__main__':

    robot_start_pos = tuple(map(int, input().split(',')))
    M1_pos = tuple(map(int, input().split(',')))
    M1_steps = int(input())
    M2_pos = tuple(map(int, input().split(',')))
    M2_steps = int(input())

    parts_M1 = int(input())
    to_collect_M1 = tuple([tuple(map(int,input().split(','))) for _ in range(parts_M1)])

    parts_M2 = int(input())
    to_collect_M2 = tuple([tuple(map(int,input().split(','))) for _ in range(parts_M2)])

    walls = [(4,0),(5,0),(7,5),(8,5),(9,5),(1,6),(1,7),(0,6),(0,8),(0,9),(1,9),(2,9),(3,9)]

    initial = (robot_start_pos[0],robot_start_pos[1],(),(),False,False,0)

    problem = Robot(initial, M1_pos, M1_steps, M2_pos, M2_steps,
                    to_collect_M1, to_collect_M2, walls)

    result = breadth_first_graph_search(problem)

    print(result.solution())
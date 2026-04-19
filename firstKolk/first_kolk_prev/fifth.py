from searching_frameworks import *

dirs={"Gore":(0,+1),"Dolu":(0,-1),"Levo":(-1,0),"Desno":(+1,0),"Stoj":(0,0)}

class Laser(Problem):
    def __init__(self, initial, target_pos, blocked,N,M):
        super().__init__(initial)
        self.target_pos = target_pos
        self.blocked = blocked
        self.width = N
        self.height = M

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]

    def goal_test(self, state):
        man_pos, timer, laser_pos = state
        return man_pos == self.target_pos

    def successor(self, state):
        successor = {}
        man_pos, timer, laser_pos = state
        px, py = man_pos

        for d in dirs:
            dx, dy = dirs[d]
            nx, ny = px + dx, py + dy
            if 0 <= nx < self.width and 0 <= ny < self.height and (nx, ny) not in self.blocked:
                new_timer = timer + 1
                if new_timer == 5:
                    new_timer = 1
                new_laser_pos = laser_pos
                if new_timer == 1:
                    new_laser_pos = (nx, ny)
                lx, ly = new_laser_pos
                if new_timer == 4:
                    if lx == nx or ly == ny:
                        continue
                successor[d] = ((nx, ny), new_timer, new_laser_pos)

        return successor


read_two = lambda: tuple(map(int, input().split()))
if __name__ == '__main__':
    N, M = read_two()
    man_pos = read_two()
    target_pos = read_two()
    timer = int(input())
    laser_pos = read_two()
    blocked = [read_two() for _ in range(int(input()))]

    initial = (man_pos, timer, laser_pos)
    problem = Laser(initial, target_pos, blocked, M, N)
    result = breadth_first_graph_search(problem)
    if result:
        print(result.solution())
    else:
        print("No Solution!")
    state = initial
    for action in result.solution():
        state = problem.result(state, action)
        print(state)
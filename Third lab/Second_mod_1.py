from searching_framework import Problem, astar_search

dir = {"Up": (0, +1), "Down": (0, -1), "Left": (-1, 0), "Right": (+1, 0)}

class Robot(Problem):
    def __init__(self, initial, goal, blocked, stations, capacity):
        super().__init__(initial, goal)
        self.blocked = set(blocked)
        self.stations = set(stations)
        self.capacity = capacity

    def successor(self, state):
        successors = {}

        robot, goal, battery = state
        r_x, r_y = robot

        for d in dir:
            dx, dy = dir[d]
            nx, ny = r_x + dx, r_y + dy
            nb = battery - 1
            if (nx, ny) not in self.blocked and nb >= 0 and 0 <= nx < 10 and 0 <= ny < 10:
                if (nx,ny) in self.stations:
                    nb = self.capacity
                if battery <= 2:
                    closer = False
                    for sx,sy in self.stations:
                        old_dist = abs(r_x - sx) + abs(r_y - sy)
                        new_dist = abs(nx - sx) + abs(ny - sy)
                        if new_dist < old_dist:
                            closer = True
                            break
                    if not closer:
                        continue
                successors[d] = ((nx,ny),goal,nb)
        return successors

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]

    def goal_test(self, state):
        robot, goal, battery = state
        r_x, r_y = robot
        return (r_x, r_y) == self.goal

    def h(self, node):
        robot, goal, battery = node.state
        gx, gy = self.goal
        r_x, r_y = robot

        return abs(r_x - gx) + abs(r_y - gy)


if __name__ == '__main__':
    blocked = [(0,6),(0,8),(0,9),(1,6),(1,7),(1,9),(2,9),(3,5),(3,9),(4,0),(5,0),(7,5),(8,5),(9,5)]
    width = 10
    height = 10
    start = tuple(map(int, input().split(",")))
    goal = tuple(map(int, input().split(",")))
    capacity = int(input())
    n = int(input())
    stations = []
    for _ in range(n):
        stations.append(tuple(map(int, input().split(","))))
    initial = (start,goal,capacity)
    problem = Robot(initial, goal, blocked, stations, capacity)
    result = astar_search(problem)
    if result is not None:
        print(result.solution())
    else:
        print("No Solution!")
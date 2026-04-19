from searching_framework import Problem, astar_search

dir = {"Up": (0, +1), "Down": (0, -1), "Left": (-1, 0), "Right": (+1, 0)}

class Robot(Problem):
    def __init__(self, initial, goal, blocked, stations, capacity, zones):
        super().__init__(initial, goal)
        self.blocked = set(blocked)
        self.stations = set(stations)
        self.capacity = capacity
        self.zones = zones

    def successor(self, state):
        successors = {}

        robot, goal, battery, used = state
        r_x, r_y = robot

        for d in dir:
            dx, dy = dir[d]
            nx, ny = r_x + dx, r_y + dy
            nb = battery - 1

            # ✅ basic validation FIRST
            if nb < 0 or not (0 <= nx < 10 and 0 <= ny < 10):
                continue

            # ✅ if zones already used → treat them as walls
            if used:
                if (nx, ny) in self.blocked or self.in_zone(nx, ny):
                    continue

                if (nx, ny) in self.stations:
                    nb = self.capacity

                successors[d] = ((nx, ny), goal, nb, used)
                continue

            # ✅ if entering zone
            if self.in_zone(nx, ny):
                slide_x = nx

                while self.in_zone(slide_x, ny):
                    slide_x += 1

                if not (0 <= slide_x < 10):
                    continue

                if (slide_x, ny) in self.blocked:
                    continue

                final_battery = nb

                if (slide_x, ny) in self.stations:
                    final_battery = self.capacity

                successors[d] = ((slide_x, ny), goal, final_battery, True)

            else:
                # normal move
                if (nx, ny) in self.blocked:
                    continue

                if (nx, ny) in self.stations:
                    nb = self.capacity

                successors[d] = ((nx, ny), goal, nb, used)

        return successors

    def in_zone(self, x, y):
        for r, x1, x2 in self.zones:
            if y == r and x1 <= x <= x2:
                return True
        return False

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]

    def goal_test(self, state):
        robot, goal, battery, used = state
        r_x, r_y = robot
        return (r_x, r_y) == self.goal

    def h(self, node):
        robot, goal, battery, used = node.state
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
    d = int(input())
    zones = []
    for _ in range(d):
        r, x1, x2 = map(int, input().split())
        zones.append((r, x1, x2))
    initial = (start, goal, capacity, False)
    problem = Robot(initial, goal, blocked, stations, capacity, zones)
    result = astar_search(problem)
    if result is not None:
        print(result.solution())
    else:
        print("No Solution!")
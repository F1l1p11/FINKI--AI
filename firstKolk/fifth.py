from searching_frameworks import Problem, breadth_first_graph_search

moves = {
    "north": {
        "Move forward":  ((0,  1), "north"),
        "Move backward": ((0, -1), "south"),
        "Turn left":     ((-1, 0), "west"),
        "Turn right":    ((1,  0), "east"),
    },
    "south": {
        "Move forward":  ((0, -1), "south"),
        "Move backward": ((0,  1), "north"),
        "Turn left":     ((1,  0), "east"),
        "Turn right":    ((-1, 0), "west"),
    },
    "east": {
        "Move forward":  ((1,  0), "east"),
        "Move backward": ((-1, 0), "west"),
        "Turn left":     ((0,  1), "north"),
        "Turn right":    ((0, -1), "south"),
    },
    "west": {
        "Move forward":  ((-1, 0), "west"),
        "Move backward": ((1,  0), "east"),
        "Turn left":     ((0, -1), "south"),
        "Turn right":    ((0,  1), "north"),
    },
}

class Packman(Problem):
    def __init__(self, initial, walls):
        super().__init__(initial)
        self.walls = walls
        self.size = 10

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]

    def goal_test(self, state):
        _, _, eat_pos = state
        return len(eat_pos) == 0

    def successor(self, state):
        successor = {}
        (x, y), direction, eat_pos = state

        for action, ((dx, dy), new_direction) in moves[direction].items():
            nx, ny = x + dx, y + dy

            if 0 <= nx < self.size and 0 <= ny < self.size and (nx, ny) not in self.walls:
                new_eat = eat_pos
                if (nx, ny) in eat_pos:
                    new_list = list(eat_pos)
                    new_list.remove((nx, ny))
                    new_eat = tuple(new_list)

                successor[action] = ((nx, ny), new_direction, new_eat)

        return successor


if __name__ == '__main__':
    x = int(input())
    y = int(input())
    man = (x, y)
    dir_man = str(input())
    number = int(input())
    eat_pos = []
    for i in range(number):
        temp = tuple(map(int, input().split(",")))
        eat_pos.append(temp)
    eat_pos = tuple(eat_pos)
    walls = [
        (0,6),(0,8),(0,9),(1,2),(1,3),(1,4),(1,9),(2,9),(3,6),(3,9),
        (4,1),(4,5),(4,6),(4,7),(5,1),(5,6),(6,0),(6,1),(6,2),(6,9),
        (8,1),(8,4),(8,7),(8,8),(9,4),(9,7),(9,8)
    ]
    initial = (man, dir_man, eat_pos)
    problem = Packman(initial, walls)
    result = breadth_first_graph_search(problem)
    if result is not None:
        print(result.solution())
    else:
        print("No Solution!")
from searching_frameworks import Problem, breadth_first_graph_search

#Move forward, Turn right, Turn left
dir = {"Move forward" : (0,-1), "Turn right" : (-1,0), "Turn left" : (+1,0)}

moves = {
    "down": {
        "Move forward":  ((0,  -1), "down"),
        "Turn right":     ((-1, 0), "left"),
        "Turn left":    ((+1,  0), "right"),
    },
    "left": {
        "Move forward":  ((-1,  0), "left"),
        "Turn right":     ((0, +1), "up"),
        "Turn left":    ((0,  -1), "down"),
    },
    "up": {
        "Move forward":  ((0,  +1), "up"),
        "Turn right":     ((+1, 0), "right"),
        "Turn left":    ((-1,  0), "left"),
    },
    "right": {
        "Move forward":  ((+1,  0), "right"),
        "Turn right":     ((0, -1), "down"),
        "Turn left":    ((0,  +1), "up"),
    },
}

class Snake (Problem):
    def __init__(self, initial, size):
        super().__init__(initial)
        self.size = size

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]

    def goal_test(self, state):
        _, pos_green, _, _ = state
        return len(pos_green) == 0

    def successor(self, state):
        successor = {}
        pos_red, pos_green, snake_position, direction = state
        for action, ((dx, dy), new_direction) in moves[direction].items():
            x, y = snake_position[len(snake_position)-1]
            nx, ny = x + dx, y + dy

            new_s = list(snake_position)
            new_s = tuple(new_s)

            if 0 <= nx < self.size and 0 <= ny < self.size and (nx, ny) not in pos_red and (nx, ny) not in new_s:
                if (nx,ny) in pos_green and (nx,ny) != snake_position[0]:
                    new_g = list(pos_green)
                    new_g.remove((nx,ny))
                    new_g = tuple(new_g)
                    new_s = list(new_s)
                    new_s.append((nx,ny))
                    new_s = tuple(new_s)
                    successor[action] = (pos_red, new_g, new_s,new_direction)
                else:
                    new_s = list(new_s)
                    new_s.append((nx,ny))
                    new_s.remove(new_s[0])
                    new_s = tuple(new_s)
                    successor[action] = (pos_red, pos_green, new_s,new_direction)

        return successor


if __name__ == '__main__':
    size = 10
    snake_position = ((0,9),(0,8),(0,7))

    number_green = int(input())
    pos_green = []
    for i in range(number_green):
        temp = tuple(map(int,input().split(",")))
        pos_green.append(temp)
    pos_green = tuple(pos_green)

    number_red = int(input())
    pos_red = []
    for i in range(number_red):
        temp = tuple(map(int,input().split(",")))
        pos_red.append(temp)
    pos_red = tuple(pos_red)

    initial = (pos_red,pos_green,snake_position,"down")
    problem = Snake (initial,size)
    solution = breadth_first_graph_search(problem)

    if solution is not None:
        print(solution.solution())
    else:
        print("No Solution!")
    state = initial
    for action in solution.solution():
        state = problem.result(state, action)
        print(state)
from searching_frameworks import Problem, breadth_first_graph_search

class HouseProblem(Problem):
    def __init__(self, initial, size, walls, house):
        super().__init__(initial)
        self.size = size
        self.walls = walls
        self.house = house

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]

    def goal_test(self, state):
        person = state
        return person == self.house

    def successor(self, state):
        successor = {}
        person = state
        x, y = person
        #up, down, left and right
        #right by two or three
        #right 3
        if x+3 < self.size and (x+3,y) not in self.walls and (x+2,y) not in self.walls and (x+1,y) not in self.walls:
            successor["Right 3"] = (x+3,y)
            successor["Right 2"] = (x+2,y)
        #right 2
        if x+2 < self.size and (x+2,y) not in self.walls and (x+1,y) not in self.walls:
            successor["Right 2"] = (x+2,y)
        #up
        if y+1 < self.size and (x,y+1) not in self.walls:
            successor["Up"] = (x,y+1)
        if y+1 < self.size and (x,y+1) not in self.walls:
            successor["Up"] = (x,y+1)
        #down
        if 0<=y-1 and (x,y-1) not in self.walls:
            successor["Down"] = (x,y-1)
        #left
        if x-1>=0 and (x-1,y) not in self.walls:
            successor["Left"] = (x-1,y)
        return successor

    def h(self, node):
        person = node.state
        x,y = person
        gx,gy = self.house
        abs_x = abs(x-gx)
        abs_y = abs(y-gy)
        return (abs_x // 3) + abs_y
if __name__ == '__main__':
    size = int(input())
    num_walls = int(input())
    walls = []
    for i in range(num_walls):
        temp = tuple(map(int, input().split(",")))
        walls.append(temp)
    person = tuple(map(int, input().split(",")))
    house = tuple(map(int, input().split(",")))
    initial = person
    problem = HouseProblem(initial, size, walls, house)
    result = breadth_first_graph_search(problem)

    if result:
        print(result.solution())
    else:
        print("No solution!")
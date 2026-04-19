from searching_frameworks import Problem, breadth_first_graph_search

dir = {"Dolu" : (0,-1), "Levo" : (-1,0)}

class Boxes(Problem):
    def __init__(self, initial, n, boxes, goal=None):
        super().__init__(initial, goal)
        self.n = n
        self.boxes = boxes

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]

    def goal_test(self, state):
        man_pos, boxes = state
        return len(boxes) == 0

    def successor(self, state):
        successor = {}
        man_pos, boxes = state
        px,py = man_pos
        for d in dir:
            dx, dy = dir[d]
            nx, ny = px+dx, py+dy
            if 0 <= nx < self.n and 0 <= ny < self.n and (nx,ny) not in self.boxes:
                flag = False
                bx,by = 0,0
                for i in [1,0,-1]:
                    for j in [1,0,-1]:
                        if (nx+i, ny + j) in boxes:
                            flag = True
                            bx,by = nx+i, ny+j
                            break
                    if flag:
                        break
                if flag:
                    new_boxes = list (boxes)
                    new_boxes.remove((bx,by))
                    new_boxes = tuple(new_boxes)
                    successor[d] = ((nx,ny), new_boxes)
                else:
                    successor[d] = ((nx,ny), boxes)
        return successor

if __name__ == '__main__':
    n = int(input())
    man_pos = (n-1, n-1)

    num_boxes = int(input())
    boxes = list()
    for _ in range(num_boxes):
        boxes.append(tuple(map(int, input().split(','))))
    boxes = tuple(boxes)

    initial = (man_pos, boxes)
    problem = Boxes(initial, n, boxes)
    solution = breadth_first_graph_search(problem)

    if solution:
        print(solution.solution())
    else:
        print("No Solution!")
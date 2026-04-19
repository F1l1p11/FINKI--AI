from searching_framework import Problem, breadth_first_graph_search

dir = {"Right": (+1, 0),"Up": (0, +1),"Left": (-1, 0),"Down": (0, -1)}

class Robot(Problem):
    def __init__(self, initial, capacity, m1_pos, m1_steps, m2_pos, m2_steps,m1_parts, m2_parts, walls):
        super().__init__(initial)
        self.capacity = capacity
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
        _, _, _, d1, d2, _, _, _ = state
        return len(d1) == len(self.m1_parts) and len(d2) == len(self.m2_parts)

    def successor(self, state):
        x, y, carry, d1, d2, M1_fixed, M2_fixed, repair = state
        successor = {}

        for d in dir:
            dx, dy = dir[d]
            nx, ny = (x + dx, y + dy)

            if 0 <= nx < 10 and 0 <= ny < 10 and (nx, ny) not in self.walls:

                new_carry = list(carry)
                new_d1 = list(d1)
                new_d2 = list(d2)

                # PICK UP parts if capacity allows
                if len(new_carry) < self.capacity:
                    if (nx, ny) in self.m1_parts and (nx, ny) not in new_carry and (nx, ny) not in new_d1:
                        new_carry.append((nx, ny))
                    elif (nx, ny) in self.m2_parts and (nx, ny) not in new_carry and (nx, ny) not in new_d2:
                        new_carry.append((nx, ny))

                # DROP parts automatically at machines
                if (nx, ny) == self.m1_pos:
                    for p in new_carry[:]:
                        if p in self.m1_parts:
                            new_d1.append(p)
                            new_carry.remove(p)

                if (nx, ny) == self.m2_pos:
                    for p in new_carry[:]:
                        if p in self.m2_parts:
                            new_d2.append(p)
                            new_carry.remove(p)

                successor[d] = (nx, ny,tuple(new_carry),tuple(new_d1),tuple(new_d2),M1_fixed,M2_fixed,0)

        # REPAIR logic
        if (x, y) == self.m1_pos and not M1_fixed and len(d1) == len(self.m1_parts):
            if repair + 1 == self.m1_steps:
                successor["Repair"] = (x, y, carry, d1, d2, True, M2_fixed, 0)
            else:
                successor["Repair"] = (x, y, carry, d1, d2, M1_fixed, M2_fixed, repair + 1)

        elif (x, y) == self.m2_pos and M1_fixed and not M2_fixed and len(d2) == len(self.m2_parts):
            if repair + 1 == self.m2_steps:
                successor["Repair"] = (x, y, carry, d1, d2, M1_fixed, True, 0)
            else:
                successor["Repair"] = (x, y, carry, d1, d2, M1_fixed, M2_fixed, repair + 1)
        return successor


if __name__ == '__main__':
    robot_start_pos = tuple(map(int, input().split(',')))
    capacity = int(input())
    M1_pos = tuple(map(int, input().split(',')))
    M1_steps = int(input())
    M2_pos = tuple(map(int, input().split(',')))
    M2_steps = int(input())
    parts_M1 = int(input())
    to_collect_M1 = tuple([tuple(map(int, input().split(','))) for _ in range(parts_M1)])
    parts_M2 = int(input())
    to_collect_M2 = tuple([tuple(map(int, input().split(','))) for _ in range(parts_M2)])

    walls = [(4, 0), (5, 0), (7, 5), (8, 5), (9, 5), (1, 6), (1, 7), (0, 6), (0, 8), (0, 9), (1, 9), (2, 9), (3, 9)]
    initial = (robot_start_pos[0], robot_start_pos[1], (), (), (), False, False, 0)
    problem = Robot(initial, capacity, M1_pos, M1_steps, M2_pos, M2_steps,to_collect_M1, to_collect_M2, walls)
    result = breadth_first_graph_search(problem)
    if result is not None:
        print(result.solution())
    else:
        print("No Solution!")
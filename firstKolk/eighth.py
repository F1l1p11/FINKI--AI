from searching_frameworks import Problem, breadth_first_graph_search

class Robot(Problem):
    def __init__(self, initial,num_fields,length_array):
        super().__init__(initial)
        self.num_fields = num_fields
        self.length_array = length_array


    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]

    def goal_test(self, state):
        expected = self.num_fields

        for i in range(self.length_array - self.num_fields, self.length_array):
            if state[i] != expected:
                return False
            expected -= 1

        return True


    def successor(self, state):
        successor = {}
        array = state
        for i in range(self.length_array):
            if array[i] != 0:
                #r1
                if i+1 < self.length_array and array[i+1] == 0:
                    array_r1 = list(array)
                    array_r1[i+1] = array[i]
                    array_r1[i] = 0
                    array_r1 = tuple(array_r1)
                    successor[f"R1: Disk {array[i]}"] = array_r1
                #r2
                if i+2 < self.length_array and array[i+1] != 0 and array[i+2] == 0:
                    array_r1 = list(array)
                    array_r1[i+2] = array[i]
                    array_r1[i] = 0
                    array_r1 = tuple(array_r1)
                    successor[f"R2: Disk {array[i]}"] = array_r1
                #l1
                if i-1 >= 0 and array[i-1] == 0:
                    array_r1 = list(array)
                    array_r1[i-1] = array[i]
                    array_r1[i] = 0
                    array_r1 = tuple(array_r1)
                    successor[f"L1: Disk {array[i]}"] = array_r1
                #l2
                if i-2 >= 0 and array[i-1] != 0 and array[i-2] == 0:
                    array_r1 = list(array)
                    array_r1[i-2] = array[i]
                    array_r1[i] = 0
                    array_r1 = tuple(array_r1)
                    successor[f"L2: Disk {array[i]}"] = array_r1

        return successor


if __name__ == '__main__':
    num_fields = int(input())
    length_array = int(input())
    array = []
    for i in range(length_array):
        if i < num_fields:
            array.append(i+1)
        else:
            array.append(0)
    array = tuple(array)
    initial = array
    problem = Robot(initial,num_fields,length_array)
    result = breadth_first_graph_search(problem)
    if result is not None:
        print(result.solution())
    else:
        print("No Solution!")
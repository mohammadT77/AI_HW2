import copy

class ACTION:
    LEFT = 'left'
    RIGHT = 'right'
    DOWN = 'down'
    UP = 'up'


def _manhattanHeuristic(state, i, j):
    x = state[i][j]
    if x == 0: x = 9
    I = lambda x: int((x - 1) / 3)

    J = lambda x: ((x % 3) - 1) % 3

    return abs(I(x) - i) + abs(J(x) - j)


def manhattanHeuristic(state):
    ary2 = state.get_2d_ary()
    return sum(_manhattanHeuristic(ary2,i,j) for i in range(3) for j in range(3))


def invcount_heur(state):
    ary1 = state.get_1d_ary()
    inv_count = 0
    for i in range(9 - 1):
        for j in range(i + 1, 9):
            if ary1[j] and ary1[i] and ary1[i] > ary1[j]:
                inv_count = inv_count + 1
    return inv_count


def is2d(ary):
    if not (type(ary)==list or  type(ary)==tuple) : return None
    return type(ary[0]) == list or type(ary[0]) == tuple

def to_1d_ary(ary2):
    return [i for j in ary2 for i in j]

def to_2d_ary(ary):
    if is2d(ary) is None: return None
    if is2d(ary): return ary
    ary2 = [ary[i*3:(i+1)*3] for i in range(3)]
    return ary2




class State:
    def __init__(self,ary):
        if type(ary)== State:
            self._ary1 = ary._ary1
            self._ary2 = ary._ary2
        elif is2d(ary) is None: raise Exception
        if is2d(ary) :
            self._ary2 = ary
            self._ary1 = to_1d_ary(ary)
        else:
            self._ary1 = ary
            self._ary2 = to_2d_ary(ary)


    def find_cell(self, item):
        for i in range(3):
            for j in range(3):
                if self._ary2[i][j] == item: return (i,j)
        return None

    def get_1d_ary(self):
        return copy.copy(self._ary1)

    def get_2d_ary(self):
        return copy.copy(self._ary2)

    def get_cost(self,heuristic=manhattanHeuristic):

        return heuristic(self)

    def __eq__(self, other):
        return str(other._ary1) == str(self._ary1)

    def __str__(self):
        return str(self._ary1)

    def Print(self):
        string = "|%d|%d|%d|\n|%d|%d|%d|\n|%d|%d|%d|" % tuple(self._ary1)
        print(string)

    def get_valid_actions(self):
        x, y = self.find_cell(0)
        return self.get_actions(x, y)

    def get_actions(self, i, j):
        if i not in [0, 1, 2] or j not in [0, 1, 2]: return None
        actions = []
        if i != 0: actions.append(ACTION.UP)
        if i != 2: actions.append(ACTION.DOWN)
        if j != 0: actions.append(ACTION.LEFT)
        if j != 2: actions.append(ACTION.RIGHT)
        return actions

    def get_succesor(self, i, j, action):
        if action not in self.get_actions(i, j): return None
        new_ary = list([list(i) for i in copy.copy(self._ary2)])

        new_i_offset = i
        new_j_offset = j

        if action == ACTION.RIGHT: new_j_offset = j + 1
        if action == ACTION.LEFT: new_j_offset = j - 1
        if action == ACTION.UP: new_i_offset = i - 1
        if action == ACTION.DOWN: new_i_offset = i + 1

        temp = new_ary[new_i_offset][new_j_offset]
        new_ary[new_i_offset][new_j_offset] = new_ary[i][j]
        new_ary[i][j] = temp

        return State(tuple([tuple(new_ary[i]) for i in range(3)]))

    def get_valid_succesores(self):
        x, y = self.find_cell(0)
        return self.get_succesores(x, y)


    def is_goal(self):

        return str(self._ary1) == str([1, 2, 3, 4, 5, 6, 7, 8, 0])

    def get_succesores(self, i, j):
        res = []
        for a in self.get_actions(i, j):
            res.append(self.get_succesor(i, j, a))

        return res


class epProblem:
    def __init__(self,state):
        if type(state)==State:
            self._startstate = state
        else:
            raise (Exception,"init type Error")

    def __str__(self):
        return str(self._startstate)

    def is_solvable(self):
        return invcount_heur(self._startstate)%2 == 0

    def __eq__(self, other):
        return str(other._startstate) == str(self._startstate)

    def get_startstate(self):
        return copy.deepcopy(self._startstate)





def generate_problem():
    l = [i for i in range(9)]
    import random
    random.shuffle(l)

    return epProblem(State(l))

def generate_problems(num):
    problems = []
    for i in range(num):
        problems.append(generate_problem())
    return problems

def hill_climbing(epproblem,heuristic=manhattanHeuristic):
    print("\n-------------------------\nTrace Start:") #TODO: trace
    # from sys import maxsize as INF
    cur = (epproblem.get_startstate())
    while not cur.is_goal():

        min_c = cur.get_cost(heuristic)
        print("Min_C:",min_c,"\tCurr:",cur) # TODO : trace
        min_ci = min_c
        min_si = cur
        for si in cur.get_valid_succesores():

            c = si.get_cost(heuristic)
            si.Print()
            print("\tmin_ci:",min_ci,"\tc:",c) # TODO : trace
            if c <= min_ci :
                min_ci = c
                min_si = si
        if min_ci <= min_c : cur = min_si
        if min_ci < min_c : min_c = min_ci
        else:
            print("\nEnd Trace\n-------------------------\n")  # TODO: trace
            return min_si
    print("\nEnd Trace\n-------------------------\n")  # TODO: trace
    return cur


def test():
    p = generate_problem()
    s = p.get_startstate()
    print("Start State:")
    s.Print()
    print("cost:",s.get_cost())
    final = hill_climbing(p)
    print("Final Cost:", final.get_cost())
    print("Final State: ", final)
    final.Print()


def test2(n):
    probs = generate_problems(n)
    count = 0
    for p in probs:
        count+=1
        print("\n============================================\n <INSTANSE #",count,">\n")
        s = p.get_startstate()
        print("Start State:")
        s.Print()
        print("cost:", s.get_cost())
        final = hill_climbing(p)
        print("Final Cost:", final.get_cost())
        print("Final State: ", final)
        final.Print()




test2(20)

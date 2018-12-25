import copy


class ACTION:
    LEFT = 'left'
    RIGHT = 'right'
    DOWN = 'down'
    UP = 'up'


def manhattanHeuristic(state, i, j):

    x = state[i][j]
    if x == 0: x = 9
    I = lambda x: int((x - 1) / 3)

    J = lambda x: ((x % 3) - 1) % 3

    return abs(I(x) - i) + abs(J(x) - j)

def invcount_heur(_ary):
    ary = [j for i in _ary for j in i]
    inv_count = 0
    for i in range(9 - 1):
        for j in range(i + 1, 9):
            if ary[j] and ary[i] and ary[i] > ary[j]:
                inv_count = inv_count + 1
    return inv_count





class Problem:

    def __init__(self,ary=[]):
        self._ary = ary


    def __str__(self):
        str = ""
        for i in self._ary:
            for j in i: str+=j
        return str



    def is_solvable(self):
        return invcount_heur(self._ary)%2 == 0

    def __eq__(self, other):
        return str(other) == str(self._ary)

    def getary(self):
        ary = copy.deepcopy(self._ary)
        return tuple([tuple(ary[i]) for i in range(3) ])


    def find_cell(self,item):
        for i in range(3):
            for j in range(3):
                if self._ary[i][j] == item : return (i,j)

        return None

    def get_valid_actions(self):
        x,y = self.find_cell(0)
        return self.get_actions(x,y)


    @staticmethod
    def to2DAry(str):
        ary = []
        # TODO: handle exeptions

        for i in range(3):
            ary.append((list(str))[i*3:(i+1)*3])

        return ary

    def get_actions(self,i,j):
        if i not in [0,1,2] or j not in [0,1,2]: return None
        actions = []
        if i != 0: actions.append(ACTION.UP)
        if i != 2: actions.append(ACTION.DOWN)
        if j != 0: actions.append(ACTION.LEFT)
        if j != 2: actions.append(ACTION.RIGHT)
        return actions

    @staticmethod
    def get_cost(state,heuristic=manhattanHeuristic):
        return sum([heuristic(state,i,j) for i in range(3) for j in range(3)])

    def get_succesor(self,i,j,action):
        if action not in self.get_actions(i,j): return None
        newAry = list([list(self.getary()[i]) for i in range(3)])

        newIOffset = i
        newJOffset = j

        if action==ACTION.RIGHT : newJOffset = j+1
        if action == ACTION.LEFT: newJOffset = j - 1
        if action == ACTION.UP: newIOffset = i - 1
        if action == ACTION.DOWN: newIOffset = i + 1

        temp = newAry[newIOffset][newJOffset]
        newAry[newIOffset][newJOffset] = newAry[i][j]
        newAry[i][j] = temp

        return tuple([tuple(newAry[i]) for i in range(3)])

    def get_valid_succesores(self):
        x,y = self.find_cell(0)
        return self.get_succesores(x,y)

    @staticmethod
    def is_goal(state):
        ary1d = [j for i in state for j in i]
        return ary1d == [1,2,3,4,5,6,7,8,0]



    def get_succesores(self,i,j):
        res = []
        for a in self.get_actions(i,j):
            res.append(self.get_succesor(i,j,a))

        return res




class SearchAgent:

    def __init__(self,problem):
        self._problem = problem






def generate_problem():
    l = [i for i in range(9)]
    import random
    random.shuffle(l)
    string=""
    for i in l:
        string = str(i)+string
    return Problem.to2DAry(string)

def generate_problems(num):
    problems = []
    for i in range(num):
        problems.append(generate_problem())
    return problems


def hill_climbing(problem,heuristic=manhattanHeuristic):
    from sys import maxsize as INF
    if not problem.is_solvable() : return None
    minCost = INF
    minS =  problem.getary()
    closed = []

    while not Problem.is_goal(minS):
        succs = {}
        def MIN(succ):
            min = INF
            Min = None
            for i in succ.keys():
                if succ[i]<min :
                    min = succ[i]
                    Min = i
            return Min
        for s in problem.get_valid_succesores():
            succs[s] = Problem.get_cost(s,heuristic)
        if len(succs) == 0: break
        minSS = MIN(succs)
        closed.append(str(minS))
        print(minCost,succs[minSS],minSS)
        if succs[minSS] <= minCost :
            print("hii")
            minCost = succs[minSS]
            minS = minSS
    return minS

def test():
    # ary = [[0,3,7], [8, 2,5], [6, 4, 1]]
    ary = [[1, 4, 3], [6,0, 5], [2, 7, 8]]
    p = Problem(ary)
    # print(p.get_cost(ary))
    h = hill_climbing(p)
    print("final",h)



# test()

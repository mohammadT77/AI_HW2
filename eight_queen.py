import copy

class ACTION:
    LEFT = 'left'
    RIGHT = 'right'
    DOWN = 'down'
    UP = 'up'

def numOfKishs(state):
    res = 0
    for i in range(8):
        j=state[i]
        for ii in range(i+1,8):
            jj=state[ii]
            if jj == j : res+=1
            elif abs(i-j) == abs(ii-jj): res+=1

    return res

def manhattanHeuristic(state, i, j):

    x = state[i][j]
    if x == 0: x = 8
    I = lambda x: int((x - 1) / 8)

    J = lambda x: ((x % 8) - 1) % 8

    return abs(I(x) - i) + abs(J(x) - j)

# def invcount_heur(_ary):
#     ary = [j for i in _ary for j in i]
#     inv_count = 0
#     for i in range(9 - 1):
#         for j in range(i + 1, 9):
#             if ary[j] and ary[i] and ary[i] > ary[j]:
#                 inv_count = inv_count + 1
#     return inv_count





class eqProblem:

    def __init__(self,ary=[]):
        self._ary = ary

    def __eq__(self, other):
        return str(other) == str(self._ary)

    @staticmethod
    def toStr(state):
        res = "   0 1 2 3 4 5 6 7\n"
        for n in range(8):
            res += str(n)+" "
            res += str("| "*state[n])
            res += "|Q|"
            res += str(" |"*(8-state[n]-1))
            res += "\n"
        return res

    @staticmethod
    def Print(state):
        print(eqProblem.toStr(state))

    def get_startstate(self):
        ary = copy.deepcopy(self._ary)
        return tuple(ary)



    @staticmethod
    def to2DAry(ary):
        ary2D = []
        # TODO: handle exeptions

        for i in ary:
            ary2D.append([1 if j == i else 0  for j in range(8)])

        return ary2D

    # def get_actions(self,i,j):
    #     if i not in range(8) or j not in range(8): return None
    #     actions = []
    #     if i != 0: actions.append(ACTION.UP)
    #     if i != 7: actions.append(ACTION.DOWN)
    #     if j != 0: actions.append(ACTION.LEFT)
    #     if j != 7: actions.append(ACTION.RIGHT)
    #     return actions


    @staticmethod
    def get_cost(state,heuristic=numOfKishs):
        return heuristic(state)

    @staticmethod
    def is_goal(state):
        return numOfKishs(state)==0

    @staticmethod
    def get_succesores(state,i):
        res = []
        cpy1 = list(copy.copy(state))
        cpy2 = list(copy.copy(state))
        if cpy1[i] < 7 :
            cpy1[i] += 1
            res.append(cpy1)
        if cpy2[i] > 0 :
            cpy2[i] -= 1
            res.append(cpy2)

        return res




class SearchAgent:

    def __init__(self,problem):
        self._problem = problem






def generate_problem():
    import random
    l = []
    for i in range(8):
        l.append(random.randint(0,7))

    return tuple(l)

def generate_problems(num):
    problems = []
    for i in range(num):
        problems.append(generate_problem())
    return problems


def hill_climbing(eqproblem,heuristic=numOfKishs):
    from sys import maxsize as INF
    cur = eqproblem.get_startstate()
    closed = []
    while not eqProblem.is_goal(cur):
        for i in range(8):
            min_s = cur
            min_c = INF
            for s in eqproblem.get_succesores(cur,i):
                if s in closed: continue
                c = eqProblem.get_cost(s)
                eqProblem.Print(s)
                if c <= min_c :
                    closed.append(s)
                    min_c = c
                    min_s = s
            cur = min_s

    return cur

def test():
    state = generate_problem()

    p = eqProblem(state)
    print(state)
    print("")
    eqProblem.Print(state)
    print(numOfKishs(state))
    print(hill_climbing(p))

test()

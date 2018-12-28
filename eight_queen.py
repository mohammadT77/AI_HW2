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
    def get_succesores(state,i,numofsuccesores=2):
        res = []
        n2 = int(numofsuccesores /2)
        cpy1 = list(copy.copy(state))
        cpy2 = list(copy.copy(state))
        for r in range(-(n2+numofsuccesores%2),n2+1):
            if r==0: continue
            cpy = list(copy.copy(state))
            cpy[i] = (cpy[i] + r) % 8
            res.append(tuple(cpy))
        # for r in range(0,n2):
        #
        # if cpy1[i] < 7 :
        #     cpy1[i] += 1
        #     res.append(cpy1)
        # if cpy2[i] > 0 :
        #     cpy2[i] -= 1
        #     res.append(cpy2)

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


def hill_climbing(eqproblem,numOfSuccesores=2,heuristic=numOfKishs):
    print("\n-------------------------\nTrace Start:") #TODO: trace
    cur = eqproblem.get_startstate()
    while not eqProblem.is_goal(cur):
        min_c = eqProblem.get_cost(cur,heuristic)
        for i in range(8):
            print("i =",i,") Min_C:",min_c,"\tCurr:",cur) # TODO : trace
            min_si = cur
            min_ci = eqProblem.get_cost(cur,heuristic)
            for si in eqproblem.get_succesores(cur,i,numOfSuccesores):
                c = eqProblem.get_cost(si,heuristic)
                print("\t",si,"\tmin_ci:",min_ci,"\tc:",c) # TODO : trace
                if c <= min_ci :
                    min_ci = c
                    min_si = si
            if min_ci <= min_c: cur = min_si
            if min_ci < min_c : min_c = min_ci
            else:
                print("\nEnd Trace\n-------------------------\n")  # TODO: trace
                return min_si
    print("\nEnd Trace\n-------------------------\n")  # TODO: trace
    return cur

def hill_climbing_multiproblem(eqproblems,numOfSuccesores=2,heuristic=numOfKishs):
    print("\n-------------------------\nTrace Start:")  # TODO: trace
    from sys import maxsize as INF
    def get_min_of_succs(State,I):
        min_state = State
        min_cost = INF
        for S in eqProblem.get_succesores(State,I,numOfSuccesores):
            C = eqProblem.get_cost(S, heuristic)
            print("\t\t", S, "\tmin_cost:", min_cost, "\tC:", C)  # TODO : trace
            if C <= min_cost:
                min_cost = C
                min_state = S
        return (min_state,min_cost)

    def get_min_of_state(State):
        min_state = State
        min_cost = INF
        for i in range(8):
            min_succ = get_min_of_succs(State,i)
            print("\ti =", i, ")",min_succ[0], "\tmin_cost:", min_cost, "\tC:", min_succ[1])  # TODO : trace
            if min_succ[1]<min_cost :
                min_cost = min_succ[1]
                min_state = min_succ[0]
        return (min_state,min_cost)

    curs = [i.get_startstate() for i in eqproblems]

    min_state = None
    min_cost = INF
    count = 0
    for cs in curs:
        count+=1
        s = get_min_of_state(cs)
        print("p =", count, ")", s[0], "\tmin_cost:", min_cost, "\tC:", s[1])  # TODO : trace
        if s[1]<min_cost:
            min_cost=s[1]
            min_state = s[0]
    print("res:",min_state)
    print("\nEnd Trace\n-------------------------\n")  # TODO: trace
    return min_state


def test1():
    state = generate_problem()
    p = eqProblem(state)
    print("Start State: ",state)
    print("numOfKishs:", numOfKishs(state),"\n")
    eqProblem.Print(state)
    final = hill_climbing(p)
    print("\nFinal State: ",final)
    eqProblem.Print(final)

def test2(numOfSuccsesores):
    state = generate_problem()
    p = eqProblem(state)
    print("Start State: ",state)
    print("numOfKishs:", numOfKishs(state),"\n")
    eqProblem.Print(state)
    final = hill_climbing(p,numOfSuccsesores)
    print("\nFinal State: ",final)
    print("numOfKishs:", numOfKishs(final), "\n")
    eqProblem.Print(final)

def test3(numOfProblems):
    states = generate_problems(numOfProblems)
    probs =  [eqProblem(s) for s in states]
    count = 0
    for p in probs:
        count+=1
        print("Problem #",count,":",p.get_startstate())
    final = hill_climbing_multiproblem(probs,7)
    print("\nFinal State: ", final)
    print("numOfKishs:", numOfKishs(final), "\n")
    eqProblem.Print(final)


test3(20)
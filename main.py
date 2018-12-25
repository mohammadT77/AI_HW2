import eight_puzzle as ep

state = [[i for i in range(8)] for j in range(8)]

string = """|%s|%s|%s|%s|%s|%s|%s|%s|
|%s|%s|%s|%s|%s|%s|%s|%s|
|%s|%s|%s|%s|%s|%s|%s|%s|
|%s|%s|%s|%s|%s|%s|%s|%s|
|%s|%s|%s|%s|%s|%s|%s|%s|
|%s|%s|%s|%s|%s|%s|%s|%s|
|%s|%s|%s|%s|%s|%s|%s|%s|
|%s|%s|%s|%s|%s|%s|%s|%s|""" % (state)


ary = [[1,2,3],[4,5,6],[7,8,0]]
a = [i for i in range(9)]
import  random
random.shuffle(a)
print(a)


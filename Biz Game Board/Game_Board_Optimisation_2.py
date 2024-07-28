from random import choice

def main():
    for rnds in range(1, 16):
        print(rnds, 'rounds :', gametester(rnds), 'squares', sep = ' ')

def gametester(rnds):
    numgames = 10000
    y = 0
    for i in range(numgames):
        y += game(rnds)
    return int(y/numgames)

def game(rnds):
    pointsumList = []
    numplayers = 5
    for i in range(numplayers):
        player(pointsumList, rnds)
    return max(pointsumList)

def player(Lst, rnds):
    s = 0
    for i in range(rnds):
        s += turn()
    Lst.append(s)

def turn():
    g = guess()
    d = points()
    return g + d

def guess():
    guess_list = [-1, 1, 2]
    g = 0
    for i in range(4):
        g += choice(guess_list)
    return g

def points():
    pointsList = []
    pointsListgenerator(pointsList)
    a = pointadd(pointsList)
    return dgen2(a)

def pointsListgenerator(Lst):
    pts = {
        -3: 3,
        -2: 3,
        -1: 4,
        1: 4,
        2: 5,
        3: 4
    }
    for i in pts:
        for j in range(pts[i]):
            Lst.append(i)
    return Lst

def pointadd(Lst):
    a = 0
    for i in range(4):
        b = choice(Lst)
        Lst.remove(b)
        a += b
    return a

def dgen(a):
    table = {
        -4: [-18, -9],
        -3: [-8, -6],
        -2: [-5, -4],
        -1: [-3, -1],
        0: [0, 0],
        1: [1, 3],
        2: [4, 5],
        3: [6, 8],
        4: [9, 18]
    }
    for l in table:
        if a >= table[l][0] and a <= table[l][1]:
            return l
        
def dgen2(a):
    numline = [-9, -6, -4, -1, 0, 3, 5, 8, 18]
    i = 0
    while a > numline[i]:
        i += 1
    return (i-4)


if __name__ == '__main__':
    main()
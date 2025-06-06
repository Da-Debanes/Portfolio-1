from queue import Queue
import random

from board import Board

class Ai:
    def __init__(self) -> None:
        self.name = "AI"
        self.matrix = []
        self.shipsquares = set()                                #Format (row, col)
        self.loadships()
        self.myboard = Board(self.matrix, self.shipsquares)
        self.oppboard = None
        self.alrhit = set()                                     #Format (row, col)
        self.win = False
        self.q = Queue()

    def in_bounds(self, r: int, c: int) -> bool:
        return 0 <= r < Board.size and 0 <= c < Board.size

    def loadships(self) -> None:
        B = Board.size
        matrix = [[0 for _ in range(B)] for _ in range(B)]
        shipsquares = set()
        i = 0

        while i < B:
            row, col = random.randint(0, B - 1), random.randint(0, B - 1)
            orientation = random.choice(["H", "V"])
            positions = []

            if orientation == "H":
                if self.in_bounds(row, col + 1):
                    positions = [(row, col), (row, col + 1)]
                else:
                    continue
            else:
                if self.in_bounds(row + 1, col):
                    positions = [(row, col), (row + 1, col)]
                else:
                    continue

            # Check overlap
            if any(p in shipsquares for p in positions):
                continue

            # Place ship
            for r, c in positions:
                matrix[r][c] = "S"
                shipsquares.add((r, c))  

            i += 1

        self.matrix = matrix
        self.shipsquares = shipsquares

    def turn(self) -> None:
        if self.q.empty():
            B = Board.size
            row, col = random.randint(0, B - 1), random.randint(0, B - 1)
            while (row, col) in self.alrhit:
                row, col = random.randint(0, B - 1), random.randint(0, B - 1)
        else:
            row, col = self.q.get()
        
        hit = self.oppboard.hit(col, row)
        self.alrhit.add((row, col))
        self.win = len(self.oppboard.shipsquares) == 0
        if hit and not self.win:
            self.addq(row, col)
            print("Hit!")
            self.oppboard.show()
            self.turn()
        
        
    def addq(self, row: int, col: int) -> None:
        dir = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        adjacent = []
        for ar, ac in dir:
            nr, nc = row + ar, col + ac
            if self.in_bounds(nr, nc) and (nr, nc) not in self.alrhit:
                adjacent.append((nr, nc))
        
        random.shuffle(adjacent)
        for move in adjacent:
            self.q.put(move)
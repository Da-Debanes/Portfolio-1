from ship import Ship

class Board:
    size = 0

    @classmethod
    def sizing(cls) -> int:
        size = int(input("Game size (3–8): "))
        while size < 3 or size > 8:
            print("Inappropriate size. The game size should be between 3 and 8.")
            size = int(input("Game size: "))
        cls.size = size
        return size

    def __init__(self) -> None:
        self.matrix = [[0 for _ in range(Board.size)] for _ in range(Board.size)]
        self.ships = set()

    def loadships(self) -> None:
        for _ in range(2):  # You can change number of ships here
            s = Ship(2, self)
            for x, y in s.nothit:
                self.matrix[y][x] = "S"
            self.ships.add(s)

    def show(self) -> None:
        header = "  " + " ".join([chr(i + 65) for i in range(Board.size)])
        print(header)
        for i in range(Board.size):
            row_str = str(i) + " "
            for j in range(Board.size):
                val = self.matrix[i][j]
                if val == 0 or val == "S":
                    row_str += "~ "
                elif val == 1:
                    row_str += "o "
                else:
                    row_str += "X "
            print(row_str)

    def hit(self, col: int, row: int) -> bool:
        hit_something = False
        for s in list(self.ships):  # use list to allow safe removal
            if s.ishit((col, row)):
                hit_something = True
                if s.issunk():
                    self.ships.remove(s)
        self.matrix[row][col] = "X" if hit_something else 1
        return hit_something

    def alrhit(self, coord: tuple[int, int]) -> bool:
        col, row = coord
        return self.matrix[row][col] in [1, "X"]

    @classmethod
    def valid_topleft(cls, pos: str, direction: str) -> bool:
        try:
            col, row = ord(pos[0].upper()) - 65, int(pos[1])
        except:
            return False
        if not (0 <= col < cls.size and 0 <= row < cls.size):
            return False
        if direction.upper() == "H" and col + 1 >= cls.size:
            return False
        if direction.upper() == "V" and row + 1 >= cls.size:
            return False
        return True


'''
class board:
    size = 0

    @classmethod
    def sizing(cls) -> int:
        size = int(input("Game size: "))
        while size < 3 or size > 8 :
            print("Inappropriate size. The game size should be between 3 and 8. Please try again")
            size = int(input("Game size: "))
        cls.size = size
        return size
    
    def __init__(self) -> None:
        self.matrix = [[0 for _ in range(board.size)] for _ in range(board.size)]
        self.ships = set()
    
    def loadships(self) -> None:
        for i in range(self.size):
            a = ship.ship(2)
            for p in a.nothit():
                self.matrix[p[1]][p[0]] = "S"
            self.ships.add(a)
    
    def show(self) -> None:
        th = "  "
        for i in range(self.size):
            th += chr(i + 65) + " "
        print(th)
        for i in range(self.size):
            st = str(i) + " "
            for j in range(self.size):
                if self.matrix[i][j] == 0 or self.matrix[i][j] == "S":
                    st += "~"
                elif self.matrix[i][j] == 1:
                    st += "o"
                else:
                    st += "X"
            print(st)

    def hit(self, col: int, row: int) -> bool:
        x = False
        for ship in self.ships:
            x = x or ship.ishit([col, row])
            if ship.issunk():
                self.ships.remove(ship)
        if x:
            self.matrix[row][col] = "X"
        else:
            self.matrix[row][col] = 1
        return x

    def alrhit(self, topleft) -> bool:
        col, row = ord(topleft[0]) - 65, int(topleft[1])
        return self.matrix[row][col] == 1 or self.matrix[row][col] == "X"

    @classmethod
    def valid_topleft(cls, topleft: str, dir: str):
        try:
            col, row = ord(topleft[0]) - 65, int(topleft[1])
        except:
            return False
        if col >= board.size or row >= board.size or col < 0 or row < 0:
            return False
        else:
            if dir == "H" and row >= board.size: 
                return False
            elif dir == "V" and col >= board.size:
                return False
        return True
        
'''

        
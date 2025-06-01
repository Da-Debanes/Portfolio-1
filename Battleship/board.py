class Board:
    size = 0

    @classmethod
    def sizing(cls) -> int:                     #Initialise size of the board
        size = int(input("Game size (3–8): "))
        while size < 3 or size > 8:
            print("Inappropriate size. The game size should be between 3 and 8.")
            size = int(input("Game size: "))
        cls.size = size
        return size

    def __init__(self) -> None:                 #Class contains the board itself as well where the ships are
        self.matrix = [[0 for _ in range(Board.size)] for _ in range(Board.size)]
        self.shipsquares = set()
        for _ in range(Board.size):  # Load 2 ships
            self.loadships(2)
            

    def loadships(self, size: int) -> None:     #Load the ships
        direction = self.get_dir()
        topleft = self.get_topleft(direction)

        new_squares = set()
        for i in range(size):
            if direction == "H":
                new_squares.add((topleft[0] + i, topleft[1]))       #Put inside set for easy access
                self.matrix[topleft[1]][topleft[0]+i] = "S"         #Show in Matrix
            else:   
                new_squares.add((topleft[0], topleft[1] + i))
                self.matrix[topleft[1] + i][topleft[0]] = "S"

        if any(sqr in self.shipsquares for sqr in new_squares):
            print("Overlap detected. Try placing again.")
            return self.loadships(size)

        self.shipsquares.update(new_squares)
        self.loadshow()                         #Draw out the board to show where they put their ships


    def show(self) -> None:                     #Show what the OPPONENT sees
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

    def loadshow(self) -> None:                 #Show what the PLAYER sees
        header = "  " + " ".join([chr(i + 65) for i in range(Board.size)])
        print(header)
        for i in range(Board.size):
            row_str = str(i) + " "
            for j in range(Board.size):
                val = self.matrix[i][j]
                if val == 0:
                    row_str += "~ "
                elif val == "S":
                    row_str += "S "
                elif val == 1:
                    row_str += "o "
                else:
                    row_str += "X "
            print(row_str)

    def hit(self, col: int, row: int) -> bool:  #Check and update if player hits ship
        if self.matrix[row][col] == "S":
            self.shipsquares.remove((col, row)) #For set of ships
            self.matrix[row][col] = "X"         #For matrix
            return True
        else:
            self.matrix[row][col] = 1
            return False

    def alrhit(self, coord: tuple[int, int]) -> bool:
        col, row = coord
        return self.matrix[row][col] in [1, "X"]

    def get_dir(self) -> str:
        direction = input("Ship direction [H for horizontal, V for vertical]: ").upper()
        while direction not in ["H", "V"]:
            print("Invalid direction.")
            direction = input("Ship direction [H/V]: ").upper()
        return direction

    def get_topleft(self, direction: str) -> tuple[int, int]:
        label = "top" if direction == "V" else "left"
        pos = input(f"Position of {label}-most part of the ship (e.g., A0): ")
        while True:
            try:
                col, row = ord(pos[0].upper()) - 65, int(pos[1])
            except:
                print("Invalid format.")
                pos = input(f"Position of {label}-most part of the ship: ")
                continue

            if not Board.valid_topleft(pos, direction):
                print("Out of bounds.")
            elif (col, row) in self.shipsquares:
                print("Position already taken.")
            else:
                break
            pos = input(f"Position of {label}-most part of the ship: ")

        return col, row
    
    @classmethod
    def valid_topleft(cls, pos: str, direction: str) -> bool:
        try:
            col, row = ord(pos[0].upper()) - 65, int(pos[1])
        except:
            return False
        if not (0 <= col < cls.size and 0 <= row < cls.size):
            return False
        if direction == "H" and col + 1 >= cls.size:
            return False
        if direction == "V" and row + 1 >= cls.size:
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

        
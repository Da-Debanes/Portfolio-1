# player.py
from board import Board

class Player:
    def __init__(self) -> None:
        #Class contains players name, their board with ships on it, their opponent's board and the status of whether they have won
        self.name = input("What is your name: ")
        self.myboard = Board()
        self.oppboard = None
        self.win = False

    def turn(self):
        move = input(f"{self.name}, enter your move (e.g., A0): ")
        while not self.valid_move(move):                #Move validation
            move = input(f"{self.name}, try again: ")
        col, row = self.make_move(move)
        hit = self.oppboard.hit(col, row)
        self.oppboard.show()
        self.win = len(self.oppboard.shipsquares) == 0  #Check for win
        if hit and not self.win:                        #Bonus Turn
            print("Hit! Go again.")
            self.turn()

    def make_move(self, move: str) -> tuple[int, int]: 
        return ord(move[0].upper()) - 65, int(move[1])

    def valid_move(self, move: str) -> bool:
        try:
            col, row = ord(move[0].upper()) - 65, int(move[1])
        except:
            print("Invalid format.")
            return False
        if not (0 <= col < Board.size and 0 <= row < Board.size):
            print("Move out of bounds.")
            return False
        if self.oppboard.alrhit((col, row)):
            print("Spot already hit.")
            return False
        return True

'''import ship

class player:
    def __init__(self) -> None:
        self.name = input("What is your name: ") 
        self.myboard = board.board()
        self.myboard.loadships()
        self.oppboard = 0
        self.win = False

    def turn(self):
        move = input(self.name +  ": ")
        while not self.valid_move(move):
            print("Not a valid move. Try again")
            move = input(self.name + ": ")
        hit = self.oppboard.hit(self.make_move(move))
        self.oppboard.show()
        self.win = self.win or len(self.oppboard.ships) == 0
        if hit and not self.win:
            self.turn()
        
    def make_move(move: str) -> tuple[int, int]:
        row, col = ord(move[0]) - 65, int(move[1])
        return row, col
    
    def valid_move(self, move: str) -> bool: 
        try:
            col, row = ord(move[0].capitalize()) - 65, int(move[1])
        except:
            print("Invalid Format")
            return False
        if col >= self.size or row >= self.size or col < 0 or row < 0:
            print("Move does not fit in the board")
            return False
        elif self.oppboard.alrhit(col, row):
            print("You have already hit this spot. Please try again")
            return False
        return True
'''
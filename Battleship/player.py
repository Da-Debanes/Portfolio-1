import os
import time

from board import Board

class Player:
    def __init__(self) -> None:
        #Class contains players name, their board with ships on it, their opponent's board and the status of whether they have won
        self.name = input("What is your name: ")
        self.myboard = Board()
        self.oppboard = None
        self.win = False
        self.clear()

    @classmethod
    def clear(self):    
        time.sleep(1)
        os.system("clear")

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

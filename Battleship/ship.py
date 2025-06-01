from board import Board

class Ship:
    def __init__(self, size: int, ownboard: Board) -> None:
        self.nothit = set()
        self.ownboard = ownboard
        direction = self.get_dir()
        topleft = self.get_topleft(direction)

        for i in range(size):
            if direction.upper() == "H":
                self.nothit.add((topleft[0] + i, topleft[1]))
            else:
                self.nothit.add((topleft[0], topleft[1] + i))

    def ishit(self, hit: tuple[int, int]) -> bool:
        if hit in self.nothit:
            self.nothit.remove(hit)
            return True
        return False

    def issunk(self) -> bool:
        return len(self.nothit) == 0

    def get_dir(self) -> str:
        direction = input("Ship direction [H for horizontal, V for vertical]: ").upper()
        while direction not in ["H", "V"]:
            print("Invalid direction.")
            direction = input("Ship direction [H/V]: ").upper()
        return direction

    def get_topleft(self, direction: str) -> tuple[int, int]:
        label = "top" if direction == "V" else "left"
        pos = input(f"Position of {label}-most part of the ship (e.g., A0): ")
        while not Board.valid_topleft(pos, direction) or self.ownboard.alrhit((ord(pos[0].upper()) - 65, int(pos[1]))):
            print("Invalid or occupied position.")
            pos = input(f"Position of {label}-most part of the ship: ")
        return ord(pos[0].upper()) - 65, int(pos[1])


'''
import board

class ship:
    def __init__(self, size: int) -> None:
        self.nothit = set()
        dir = self.get_dir()
        topleft = self.get_topleft(dir)

        for i in range(size):
            if dir == "H":
                self.nothit.add([topleft[0] + i, topleft[1]])
            else:
                self.nothit.add([topleft[0], topleft[1] + i])

    def ishit(self, hit: tuple[int, int]) -> bool:
        if hit in self.nothit:
            self.nothit.remove(hit)
            return True
        return False
    
    def issunk(self):
        return len(self.nothit) == 0
    
    def get_dir(self):
        dir = input("State the direction of your ship [H for horizontal, V for vertical]: ")
        while dir.capitalize() != "H" and dir.capitalize() != "V":
            print("Not a valid direction.")
            dir = input("State the direction of your ship [H for horizontal, V for vertical]: ")
        return dir
    
    def get_topleft(self, dir: str) -> tuple[int, int]:
        top_or_left = "top" if dir == "V" else "left"
        topleft = input("State the position of the " + top_or_left + "most part of your ship: ")
        while not board.valid_topleft(topleft, dir) or self.ownboard.alrhv(topleft):
            print("Not a valid ship. Please try again")
            topleft = input("State the position of the " + top_or_left + "most part of your ship: ")
        
        col, row = ord(topleft[0]) - 65, int(topleft[1])
        return col, row

'''

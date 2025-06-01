from player import Player
from board import Board

def main():
    Board.sizing()

    player1 = Player()
    player2 = Player()

    player1.oppboard = player2.myboard
    player2.oppboard = player1.myboard

    while (not player1.win and not player2.win):
        player1.turn()
        if not player1.win:
            player2.turn()

    winner = player1.name if player1.win else player2.name
    
    print("Game Over. Winner is: " + winner)

if __name__ == "__main__":
    main()

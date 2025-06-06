from player import Player
from board import Board
from AI import Ai

def main():
    Board.sizing() #Determine the size of the game. 

    #Initialise the players
    player1 = Player()
    p2 = input("Do you wish to play against AI? Double Player Mode otherwise. [y/n]: ")
    player2 = Player() if p2.upper() == "N" else Ai()

    #Assign competitve relationship between the boards of the 2 players
    player1.oppboard = player2.myboard
    player2.oppboard = player1.myboard

    #Enables turn by turn unless one player wins indefinitely
    while (not player1.win and not player2.win):
        player1.turn()
        Player.clear()
        if not player1.win:
            player2.turn()
            Player.clear()

    winner = player1.name if player1.win else player2.name
    
    #End of game
    print("Game Over. Winner is: " + winner)

if __name__ == "__main__":
    main()

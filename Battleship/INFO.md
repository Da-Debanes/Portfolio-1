First OOP based project - creating commandline version of the game, Battleship

The project uses 3 supporting classes:
1. Board which contains all the information about what is on the board itself including the ships and how they are hit
2. Player which contains the names and functionality of turns and winning
3. AI which contains almost the same functionality as Player just that it uses a random + queue algorithm to play the game.

Initially, the project had a 3rd class which were the Ship. However, Python does not support circular dependence between board and ship due to which it had to be removed. Lesson learnt: Classes need to follow an upwards pattern

AFI: Find whether it would be more appropriate to segment the project into more classes
AFI: Optimise the algorithm such that after it finds the adjacent it doesnt go through the rest of them as well.

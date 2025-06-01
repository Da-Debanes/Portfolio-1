First OOP based project - creating commandline version of the game, Battleship

The project uses 2 supporting classes:
1. Board which contains all the information about what is on the board itself including the ships and how they are hit
2. Player which contains the names and functionality of turns and winning

Initially, the project had a 3rd class which were the Ship. However, Python does not support circular dependence between board and ship due to which it had to be removed. Lesson learnt: Classes need to follow an upwards pattern

AFI: Find whether it would be more appropriate to segment the project into more classes

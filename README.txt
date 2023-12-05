This Battleship AI was developed in Dec 2023 for Virginia Tech's Intro to AI Course
By Jasper Wilkerson and Jade Sherer

How to use:
This program has a few different options for games
All of these options can be changed in constants.py
Here are some options you may want to change

TICKRATE -how fast the lag time between moves is for the AI

HUMAN1 HUMAN2 -these two parameters determine how many humans will be playing 
                Set both to False for AI vs AI, both to True for human vs human

HIDEBOARD -this determines whether to hide ships on the bottom part of the screen

COMPUTER1 COMPUTER2 -these two parameters determine which type of AI will be used for each player
                    Options include: Random, RandomHunt, RandomSmartHunt, Parity, Heat
                    These are detailed below

AUTORESTART -determines if the game automatically restarts on win. Used to gather data

To Start: python gui.py
Yours and your opponent's ships will be randomly placed
If any HUMAN# is set to True, you may click on the desired spot to fire a missile on your turn
The spacebar will pause the game, esc will exit the game

AIs:
Random: a simply random AI. This ai will not hunt ships and will only fire in places it has not yet fired

RandomHunt: a random AI that will hunt ships on hit. 

RandomSmartHunt: a random AI that will hunt ships on hit using the information about previous hits to intelligently fire

Parity: will fire in a random diagonal pattern, and will hunt ships on hit intelligently

Heat: calculates possible ship configurations, then generates a heatmap based on the most likely position
        Note: Heat AI is experimental and high performance. 
        It is not recommended to player Human vs Heat AI, since ship placements can often be unlucky 
        and take upwards of 5 minutes per move. 
        If you do choose to play against Heat AI, please select your move and be patient, 
        as it may take some time for the board to update.  

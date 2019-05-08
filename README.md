# AI_learnToDrift_2D

Team 10 Members:  
Gordon Huynh  
Jimmy Xuan  
Eric Le  
Duy Do  


# Description

AI_learnToDrift_2D is a simulation of a car that learns to drive around a track through
Q-learning (reinforcement learning), programmed in Python 3. The following files should 
be present..

  - mainWindow.py: Initializes the graphical interface, keyboard controls,
		   training data management, and imports other files.
 
  - CarSprite.py: Contains the CarSprite() class, which contains the initialization of the 
		  car sprite, implementation of car rotation, actions/states and their
	          respective reward values, as well as checkpoints and collision detection.

  - AI.py: Contains various variables for the Bellman's equation, initializes the q-table
	   and training function, and storing of the previous 4 moves to prevent looping.

  - Grid.py: Draws the hidden grid for the track in order to keep track of car actions.

  - Line.py: Initializes Line() class that streamlines the line drawings.

  - Track.py: Draws the track in which the car will proceed along.


# Instructions

To test the project, run the following commands in a Linux terminal to download the required libraries..

   > pip install --user pyglet  
   > pip install --user numpy  

Head to  https://avbin.github.io/AVbin/Download.html and download AVbin10 for Linux and run the following command in your terminal to install it.

   > sudo sh ./install-avbin-linux-x86-64-v10  

If you do not have Python 3 installed on your terminal, run the following command to do so..

   > sudo apt-get install python3.6

Once the required libraries are installed, run the following command in the terminal opened in the appropriate directory..

   > python3 mainWindow.py 

Press "Enter" to begin training the car. If you wish to view the grid, you may toggle the 
display by pressing "G"


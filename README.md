# Glimmer-Solver
Solver script for Glimmer &amp; Gloom written in python

![Demonstration clip of the solver in use.](https://github.com/dcom365/Glimmer-Solver/assets/10088267/42b8e5ea-8f46-4c51-8069-ae902cdcafb3)

## Setup Guide
Setup guide currently only includes Windows. If anyone would like to add instructions for MacOS and Linux please let me know.  
### Windows
1. Install [Python](https://www.python.org/downloads/) if you do not have it (I used 3.10.5 to make this, I imagine other versions will work but I haven't tried)
2. Click on the code dropdown button and click on download zip
4. Exract the zip in a folder of your choice and open the folder in explorer
5. Click on the address bar and type `cmd` and press enter to open the command prompt
6. Type `pip install -r requirements.txt` into command prompt to install the depencies needed to run the script

## Usage Guide
For best results, keep your web browser at default zoom level  
1. Open the folder you extracted the zip to and open the command prompt
2. Start a game of Glimmer &amp; Gloom on the very hard difficulty
3. Make sure the Glimmer &amp; Gloom game window is not blocked by any other windows (See demonstration clip for an example)
4. Type `py solver.py` into the command prompt, it should give a result similar to this:  
![image](https://github.com/dcom365/Glimmer-Solver/assets/10088267/b512f478-4461-4429-b6d6-a5d86f6d091e)
5. The '*' correspond to the tiles you need to click on, in this example I would need to click on the 2nd and 3rd tile in the top row
6. Solve through the board as [usual](https://www1.flightrising.com/forums/gde/2765443/3#post_42869083). However, instead of going off shadow cells go off of light cells instead as the script will always try to solve for shadow winning instead of light
7. Upon completing the board, after starting a new game you can press the up arrow key followed by the enter key to quickly run the script again

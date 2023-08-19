import numpy as np
from PIL import ImageGrab, Image
import cv2

count = 0
thresh = 0.65
nms_thres = 0.9
tiles = []
gameboard = [
			[None] * 5,
			[None] * 6,
			[None] * 7,
			[None] * 8,
			[None] * 9,
			[None] * 8,
			[None] * 7,
			[None] * 6,
			[None] * 5,
		]

solution = [0,0,0,0,0,0,0,0,0]
solution_pattern = [0,0,0,0,0,0,0,0,0]

def Flip(t,r,c):
    if t[r][c] == 1:
        t[r][c] = 0
    else:
        t[r][c] = 1

def FindSolution():
    board_patterns = (
	(0, 0, 0, 1, 0, 1, 0, 0, 1),
	(0, 0, 0, 0, 1, 1, 1, 1, 0),
	(0, 0, 1, 1, 0, 1, 0, 1, 0),
	(1, 0, 1, 1, 0, 1, 1, 1, 1),
	(0, 1, 0, 0, 1, 0, 0, 1, 0),
	(1, 1, 1, 1, 0, 1, 1, 0, 1),
	(0, 1, 0, 1, 0, 1, 1, 0, 0),
	(0, 1, 1, 1, 1, 0, 0, 0, 0),
	(1, 0, 0, 1, 0, 1, 0, 0, 0)
)
    for i in range(len(finalboard)):
        if finalboard[i] == 1:
            solution_pattern = board_patterns[i]
            for x in range(len(solution_pattern)):
                if solution[x] == 1 and solution_pattern[x] == 1:
                    solution[x] = 0
                elif solution_pattern[x] == 1:
                    solution[x] = 1
    for i in range(len(solution)):
        if solution[i] == 1:
            if i == 0:
                gameboard[4][0] = "*"
            elif i == 1:
                gameboard[3][0] = "*"
            elif i == 2:
                gameboard[2][0] = "*"
            elif i == 3:
                gameboard[1][0] = "*"
            elif i == 4:
                gameboard[0][0] = "*"
            elif i == 5:
                gameboard[0][1] = "*"
            elif i == 6:
                gameboard[0][2] = "*"
            elif i == 7:
                gameboard[0][3] = "*"
            elif i == 8:
                gameboard[0][4] = "*"
            elif i == 9:
                gameboard[0][5] = "*"

    for q in range(len(gameboard[0:5])):
        if q == 0 or q == 8:
            indents = "     "
        elif q == 1 or q == 7:
            indents = "    "
        elif q == 2 or q == 6:
            indents = "   "
        elif q == 3 or q == 5:
            indents = "  "
        else:
            indents = ""
        print(indents, gameboard[q])

#Loading images, screen takes SS of main monitor, templates are loaded from drive
screen = np.array(ImageGrab.grab())
glimmer = cv2.imread("img/glimmer.png")
gloom = cv2.imread("img/gloom.png")

#Converting all images to mat-like and grayscale
glimmer_gray = cv2.cvtColor(glimmer, cv2.COLOR_BGR2GRAY)
gloom_gray = cv2.cvtColor(gloom, cv2.COLOR_BGR2GRAY)
screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

#Defining template dimensions for rectangles
template_h, template_w = glimmer.shape[:-1]

#run template matching
glimmer_out = cv2.matchTemplate(screen_gray, glimmer_gray, cv2.TM_CCOEFF_NORMED)
gloom_out = cv2.matchTemplate(screen_gray, gloom_gray, cv2.TM_CCOEFF_NORMED)

#create arrays for matched points
glim_y_coords, glim_x_coords = np.where(glimmer_out >= thresh)
gloo_y_coords, gloo_x_coords = np.where(gloom_out >= thresh)

glim_box = np.array([[x,y,x+template_w,y+template_h]
                     for (x, y) in zip(glim_x_coords,glim_y_coords)])

glim_indices = cv2.dnn.NMSBoxes(glim_box, glimmer_out[glim_y_coords,glim_x_coords], thresh, nms_thres)

for i in glim_indices:
    (x,y,w,h) = glim_box[i][0], glim_box[i][1], glim_box[i][2], glim_box[i][3]
    #Tiles will store all tiles
    tiles.append([glim_box[i][0],glim_box[i][1],1])

gloo_box = np.array([[x,y,x+template_w,y+template_h]
                     for (x, y) in zip(gloo_x_coords,gloo_y_coords)])

gloo_indices = cv2.dnn.NMSBoxes(gloo_box, gloom_out[gloo_y_coords,gloo_x_coords], thresh, nms_thres)

for i in gloo_indices:
    (x,y,w,h) = gloo_box[i][0], gloo_box[i][1], gloo_box[i][2], gloo_box[i][3]
    #Tiles will store all tiles
    tiles.append([gloo_box[i][0],gloo_box[i][1],0])

#Sorting out tiles list by Y coord followed by X Coord
tiles = sorted(tiles, key=lambda x: (x[1], x[0]))
#Resort the middle row for some reason?
tiles[26:35] = sorted(tiles[26:35])

#Row tracking, this is ugly but it .. works
row1 = 0
row2 = 0
row3 = 0
row4 = 0
row5 = 0
row6 = 0
row7 = 0
row8 = 0
row9 = 0

#Check tile count
if len(tiles) > 61:
    print("Error: Too many board tiles detected. This will cause inaccurate results.")
    print("The script has been stopped. Please raise the thresh value before running again.")
    exit()
elif len(tiles) < 61:
    print("Error: Not enough board tiles detected. This will cause inaccurate results.")
    print("The script has been stopped. Please lower the thresh value before running again.")
    exit()

#Convert tiles to gameboard
while count < len(tiles):
#Row 1
    if count < 5:
        if tiles[count][2] == 1:
            gameboard[0][row1] = 1
            row1 += 1
        elif tiles[count][2] == 0:
            gameboard[0][row1] = 0
            row1 += 1
    #Row 2
    elif count >= 5 and count < 11:
        if tiles[count][2] == 1:
            gameboard[1][row2] = 1
            row2 += 1
        elif tiles[count][2] == 0:
            gameboard[1][row2] = 0
            row2 += 1
    #Row 3
    elif count >= 11 and count < 18:
        if tiles[count][2] == 1:
            gameboard[2][row3] = 1
            row3 += 1
        elif tiles[count][2] == 0:
            gameboard[2][row3] = 0
            row3 += 1
    #Row 4
    elif count >= 18 and count < 26:
        if tiles[count][2] == 1:
            gameboard[3][row4] = 1
            row4 += 1
        elif tiles[count][2] == 0:
            gameboard[3][row4] = 0
            row4 += 1
    #Row 5
    elif count >= 26 and count < 35:
        if tiles[count][2] == 1:
            gameboard[4][row5] = 1
            row5 += 1
        elif tiles[count][2] == 0:
            gameboard[4][row5] = 0
            row5 += 1
    #Row 6
    elif count >= 35 and count < 43:
        if tiles[count][2] == 1:
            gameboard[5][row6] = 1
            row6 += 1
        elif tiles[count][2] == 0:
            gameboard[5][row6] = 0
            row6 += 1
    #Row 7
    elif count >= 43 and count < 50:
        if tiles[count][2] == 1:
            gameboard[6][row7] = 1
            row7 += 1
        elif tiles[count][2] == 0:
            gameboard[6][row7] = 0
            row7 += 1
    #Row 8
    elif count >= 50 and count < 56:
        if tiles[count][2] == 1:
            gameboard[7][row8] = 1
            row8 += 1
        elif tiles[count][2] == 0:
            gameboard[7][row8] = 0
            row8 += 1
    #Row 9
    elif count >= 56 and count < 61:
        if tiles[count][2] == 1:
            gameboard[8][row9] = 1
            row9 += 1
        elif tiles[count][2] == 0:
            gameboard[8][row9] = 0
            row9 += 1
    
    count += 1

#Cols i
for i in range(len(gameboard)):
    #Rows x
    for x in range(len(gameboard[i])):
        #Check if tile is glimmer
        if gameboard[i][x] == 1:
            if i <= 3:
                tempCol = x + 1
                tempRow = i + 1
            else:
                tempCol = x
                tempRow = i + 1
            #Top half rules
            if i < 3:
                Flip(gameboard, tempRow - 1, tempCol - 1)
                Flip(gameboard, tempRow, tempCol - 1)
                Flip(gameboard, tempRow, tempCol)
                Flip(gameboard, tempRow + 1, tempCol)
                Flip(gameboard, tempRow + 1, tempCol + 1)
                try:
                    Flip(gameboard, tempRow-1, tempCol)
                    Flip(gameboard, tempRow, tempCol+1)
                except:
                    pass
            #Additional try rule for middle row
            elif i == 3:
                Flip(gameboard, tempRow - 1, tempCol - 1)
                Flip(gameboard, tempRow, tempCol)
                Flip(gameboard, tempRow, tempCol-1)
                Flip(gameboard, tempRow + 1, tempCol - 1)
                try:
                    Flip(gameboard, tempRow+1, tempCol)
                    Flip(gameboard, tempRow-1, tempCol)
                    Flip(gameboard, tempRow, tempCol+1)
                except:
                    pass
            #Specific rules for final row         
            elif i == 7:
                if x == 5:
                    pass
                else:
                    Flip(gameboard, tempRow-1, tempCol)
                    Flip(gameboard, tempRow-1, tempCol+1)
                    Flip(gameboard, tempRow, tempCol)
                    #Ride side failsafe
                    if tempCol -1 != -1:
                        Flip(gameboard, tempRow, tempCol-1)
                    #Right side failsafe
                    if tempCol + 2 > len(gameboard[tempRow]):
                        pass
                    else:
                        Flip(gameboard, tempRow, tempCol+1)
            #Nothing to do on row 8
            elif i == 8:
                pass
            #Bottom half rules
            else:
                if x == 8:
                    pass
                elif x == 7 and i == 5:
                    pass
                elif x == 6 and i == 6:
                    pass
                elif x == 5 and i == 7:
                    pass
                else:
                    Flip(gameboard, tempRow-1, tempCol)
                    Flip(gameboard, tempRow-1, tempCol+1)
                    Flip(gameboard, tempRow, tempCol)
                    #Left side failsafe
                    if tempCol -1 != -1:
                        Flip(gameboard, tempRow, tempCol-1)
                        Flip(gameboard, tempRow+1, tempCol-1)
                    #Right side failsafe
                    if tempCol + 2 > len(gameboard[tempRow]):
                        pass
                    else:
                        Flip(gameboard, tempRow, tempCol+1)
                        Flip(gameboard, tempRow+1, tempCol)

finalboard = gameboard[8]
finalboard.append(gameboard[7][5])
finalboard.append(gameboard[6][6])
finalboard.append(gameboard[5][7])
finalboard.append(gameboard[4][8])

FindSolution()


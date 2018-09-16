# coding=utf-8
import numpy as np
import random as rand 
import os
import time
import math
import numpy as np
import pyscreenshot as ImageGrab
import cv2


#config variables
row=20
col=10
CurrentPiece = np.arange(row*col)
CurrentPiece = CurrentPiece.reshape(row, col)
TetrisGame = np.arange(row*col)
TetrisGame = TetrisGame.reshape(row, col)
TryTetrisGame = np.arange(row*col)
TryTetrisGame = TryTetrisGame.reshape(row, col)

DebugGame = np.arange(row*col)
DebugGame = DebugGame.reshape(row, col)
point=0

HighestYs = [19 for i in range(0,10)]


TryLineWereCleard=0

botReward=0
pointOverGames=0

timeslost=0

#BotValues

fuzziness = [0 for i in range(0,9)]

TheBrick=0

#Bot Values
roughness = 0

patternMinimum = 0
sumAll = 0

#pieces 0gul,1rød, 2grøn, 3blå, 4orange, 5lilla, 6lyseblå
piece=5
rotation=0


def init():
	
	global point
	resetWholeGame()

def GetAllPatterns(GameArray):
	GetHighestYs(GameArray) #set the global HighestYs array
	GetFuzziness(GameArray)
	GetRoughness(GameArray)
	return GetFuzziness(GameArray),GetRoughness(GameArray)
	
def GetHighestYs(GameArray):
	global HighestYs
	HighestYs = [19 for i in range(0,10)]
	for x in range(9, -1, -1):
		for y in range(19, -1, -1):
			if(GameArray[y][x] == 1):
				HighestYs[x]=y
	for x in range(len(HighestYs)):
		if HighestYs[x] == 19:
			if GameArray[19][x] ==0:
				HighestYs[x]=20
			else:
				HighestYs[x]=19
	return 0
	
def GetFuzziness(GameArray):
	global HighestYs
	global fuzziness
	fuzz=0
	for x in range(0,9):
		fuzziness[x]=abs(HighestYs[x]-HighestYs[x+1])
		fuzz=fuzz+fuzziness[x]
	return fuzz
	
def GetRoughness(GameArray):
	global HighestYs
	global roughness
	roughness=0
	for x in range(col):
		for y in range(ReverseNumber(19,HighestYs[x])):
			if HighestYs[x] == 20:
				break
			if GameArray[ReverseNumber(19,y)][x] == 0:
					roughness=roughness+1
	return roughness
	
def ReverseNumber(Range, Number):
	return abs(Range-Number)

def GetLowestRoughAndFuzz():
	return 0
	
def GivePoints(NumLinesCleared):
	global point
	global pointOverGames
	if NumLinesCleared == 1:
		point = point+1
		pointOverGames =pointOverGames+1
	if NumLinesCleared == 2:
		point = point+3
		pointOverGames =pointOverGames+2
	if NumLinesCleared == 3:
		point = point+6
		pointOverGames =pointOverGames+3
	if NumLinesCleared == 4:
		point = point+10
		pointOverGames=pointOverGames+4
	
def CheckWallCollision():
	count=0
	array=[0,0,0,0]
	for y in range(row):
		for x in range(col):
			if CurrentPiece[y][x] == 1:
				array[count]=x
				count=count+1
	
	if(array[0]-array[0]) > -4 and (array[0]-array[0]) < 4:
		if(array[0]-array[1]) > -4 and (array[0]-array[1]) < 4:
			if(array[0]-array[2]) > -4 and (array[0]-array[2]) < 4:
				if(array[0]-array[3]) > -4 and (array[0]-array[3]) < 4:
					return False
	return True

def IsGameLost():
	IsItLost=False
	for x in range(col):
		for y in range(0,4):
			if TetrisGame[y][x] == 1:
				IsItLost=True
	return IsItLost
	
def GiveNewPiece():

	global TheBrick
	global piece
	global rotation
	
	if TheBrick == "gul":
		piece=0
	if TheBrick == "rød":
		piece=1
	if TheBrick == "grøn":
		piece=2
	if TheBrick == "blå":
		piece=3
	if TheBrick == "orange":
		piece=4
	if TheBrick == "lilla":
		piece=5
	if TheBrick == "lyseblå":
		piece=6
	
	rotation=0
	Rotate()

def resetWholeGame():
	global point
	point=0
	for x in range(col):
		for y in range(row):
			CurrentPiece[y][x]=0
			TetrisGame[y][x]=0
	Rotate()
	
def ResetCurrentPiece():
	for x in range(col):
		for y in range(row):
			CurrentPiece[y][x]=0
	
def Rotate():
	global piece
	global rotation
	ResetCurrentPiece()
	#gul
	if piece==0: 
		CurrentPiece[0][4]=1
		CurrentPiece[0][5]=1
		CurrentPiece[1][4]=1
		CurrentPiece[1][5]=1
		
	#rød
	if piece==1: 
		if rotation == 0 or rotation==2:		
			CurrentPiece[0][3]=1
			CurrentPiece[0][4]=1
			CurrentPiece[1][4]=1
			CurrentPiece[1][5]=1		
		if rotation == 1 or rotation==3:	
			CurrentPiece[0][5]=1
			CurrentPiece[1][5]=1
			CurrentPiece[1][4]=1
			CurrentPiece[2][4]=1
				
	#grøn
	if piece==2: 
		if rotation == 0 or rotation==2:
			CurrentPiece[1][3]=1
			CurrentPiece[1][4]=1
			CurrentPiece[0][4]=1
			CurrentPiece[0][5]=1
		if rotation == 1 or rotation==3:		
			CurrentPiece[0][4]=1
			CurrentPiece[1][4]=1
			CurrentPiece[1][5]=1
			CurrentPiece[2][5]=1

	
	#blå
	if piece==3: 
		if rotation == 0:		
			CurrentPiece[0][3]=1
			CurrentPiece[1][3]=1
			CurrentPiece[1][4]=1
			CurrentPiece[1][5]=1
		if rotation == 1:		
			CurrentPiece[0][4]=1
			CurrentPiece[1][4]=1
			CurrentPiece[2][4]=1
			CurrentPiece[0][5]=1
		if rotation == 2:		
			CurrentPiece[0][3]=1
			CurrentPiece[0][4]=1
			CurrentPiece[0][5]=1
			CurrentPiece[1][5]=1
		if rotation == 3:		
			CurrentPiece[0][4]=1
			CurrentPiece[1][4]=1
			CurrentPiece[2][4]=1
			CurrentPiece[2][3]=1
	
	#orange
	if piece==4:
		if rotation == 0:
			CurrentPiece[0][5]=1
			CurrentPiece[1][5]=1
			CurrentPiece[1][4]=1
			CurrentPiece[1][3]=1
		if rotation == 1:
			CurrentPiece[0][4]=1
			CurrentPiece[1][4]=1
			CurrentPiece[2][4]=1
			CurrentPiece[2][5]=1
		if rotation == 2:
			CurrentPiece[0][3]=1
			CurrentPiece[0][4]=1
			CurrentPiece[0][5]=1
			CurrentPiece[1][3]=1
		if rotation == 3:
			CurrentPiece[0][4]=1
			CurrentPiece[1][4]=1
			CurrentPiece[2][4]=1
			CurrentPiece[0][3]=1

	#lilla
	if piece==5:
		if rotation == 0:
			CurrentPiece[1][3]=1
			CurrentPiece[1][4]=1
			CurrentPiece[1][5]=1
			CurrentPiece[0][4]=1
		if rotation == 1:
			CurrentPiece[0][4]=1
			CurrentPiece[1][4]=1
			CurrentPiece[1][5]=1
			CurrentPiece[2][4]=1
		if rotation == 2:
			CurrentPiece[0][3]=1
			CurrentPiece[0][4]=1
			CurrentPiece[1][4]=1
			CurrentPiece[0][5]=1
		if rotation == 3:
			CurrentPiece[0][4]=1
			CurrentPiece[0][4]=1
			CurrentPiece[1][4]=1
			CurrentPiece[1][3]=1
			CurrentPiece[2][4]=1

	#lyseblå
	if piece==6: 
		if rotation == 0 or rotation==2:		
			CurrentPiece[0][3]=1
			CurrentPiece[0][4]=1
			CurrentPiece[0][5]=1
			CurrentPiece[0][6]=1
		if rotation == 1 or rotation==3:		
			CurrentPiece[0][5]=1
			CurrentPiece[1][5]=1
			CurrentPiece[2][5]=1
			CurrentPiece[3][5]=1
	
def RightMove(times,piece):
	global CurrentPiece	
	for i in range(times):
		CurrentPiece=np.roll(CurrentPiece,1, axis=1)
		if CheckWallCollision() == True:
			CurrentPiece=np.roll(CurrentPiece,-1, axis=1)
		if piece== 6 and CurrentPiece[0][0] == 1:
			CurrentPiece=np.roll(CurrentPiece,-1, axis=1)
		
def LeftMove(times, piece):
	global CurrentPiece
	for i in range(times):
		CurrentPiece=np.roll(CurrentPiece,-1, axis=1)
		if CheckWallCollision() == True:
			CurrentPiece=np.roll(CurrentPiece,1, axis=1)
		#fix for lyseblå collisons med væg brik	
		if piece== 6 and CurrentPiece[0][9] == 1:
			CurrentPiece=np.roll(CurrentPiece,1, axis=1)
			
def CheckCollision():
	global CurrentPiece
	BundHit=False
	for y in range(row):
		for x in range(col):
			if CurrentPiece[y][x] == TetrisGame[y][x] and TetrisGame[y][x] == 1:
				CurrentPiece=np.roll(CurrentPiece,-1, axis=0)
				MergeGame()
				return True
			if y==19 and CurrentPiece[y][x] == 1:
				BundHit=True
	if BundHit == True:
		MergeGame()
		return True
	return False

def MergeGame():
	global point
	global timeslost
	for y in range(row):
		for x in range(col):
			if CurrentPiece[y][x] == 1:	
				TetrisGame[y][x] = 1
	ResetCurrentPiece()
	CheckForLineClear()
	if IsGameLost() == True:
		timeslost += 1
		# print('Game Over')
		# print('Bot Has Played: ',timeslost,' Games')
		resetWholeGame()

def CheckForLineClear():
	numLinesCleared=0
	checkLineCleared=0
	linesCleared = [0] * 20
	for y in range(row):
		for x in range(col):
			if TetrisGame[y][x] == 1:
				checkLineCleared=checkLineCleared+1
		if checkLineCleared==10:
			numLinesCleared=numLinesCleared+1
			linesCleared[y]=1
		checkLineCleared=0
	
	if numLinesCleared >= 1:
		LineCleared(linesCleared,numLinesCleared)

def LineCleared(LineClearArray,NumLinesCleared):
	for y in range(row):
		for x in range(col):
			if LineClearArray[y] == 1:
				TetrisGame[y][x]=0
	GravityClearedLines(LineClearArray,NumLinesCleared)
	GivePoints(NumLinesCleared)

def GravityClearedLines(LineClearArray,NumLinesCleared):
	lowestLine=0
	for i in range(len(LineClearArray)):
		if LineClearArray[i] == 1:
			lowestLine=i
	
	for i in range(NumLinesCleared):
		for y in range(lowestLine,0,-1):
			for x in range(col):
				if  y !=0:
					TetrisGame[y][x] = TetrisGame[y-1][x]

def Drop():
	Collision=False
	while (Collision == False):
		global CurrentPiece
		CurrentPiece=np.roll(CurrentPiece,1, axis=0)
		Collision=CheckCollision()
	GiveNewPiece()

def Debug():
	global CurrentPiece
	global TetrisGame
	global DebugGame
	
	for x in range(col):
		for y in range(row):
			DebugGame[y][x]=0	
	
	for x in range(col):
		for y in range(row):
			if CurrentPiece[y][x] == 1:	
				DebugGame[y][x] = 1

	for x in range(col):
		for y in range(row):
			if TetrisGame[y][x] == 1:	
				DebugGame[y][x] = 1
	print(DebugGame)

#try funcs makes copy of the game
# to try and make moves and see if they are good or bad
# then it goes back to the original game and does the best move. 
# so a way to look a step ahead in the future. 
	
def TryCheckCollision():
	global CurrentPiece
	BundHit=False
	for y in range(row):
		for x in range(col):
			if CurrentPiece[y][x] == TryTetrisGame[y][x] and TryTetrisGame[y][x] == 1:
				CurrentPiece=np.roll(CurrentPiece,-1, axis=0)
				TryMergeGame()
				return True
			if y==19 and CurrentPiece[y][x] == 1:
				BundHit=True
	if BundHit == True:
		TryMergeGame()
		return True
	return False
		
def TryMergeGame():
	global point
	global timeslost
	for y in range(row):
		for x in range(col):
			if CurrentPiece[y][x] == 1:	
				TryTetrisGame[y][x] = 1

def TryCheckForLineClear():
	numLinesCleared=0
	checkLineCleared=0
	linesCleared = [0] * 20
	for y in range(row):
		for x in range(col):
			if TryTetrisGame[y][x] == 1:
				checkLineCleared=checkLineCleared+1
		if checkLineCleared==10:
			numLinesCleared=numLinesCleared+1
			linesCleared[y]=1
		checkLineCleared=0
	
	if numLinesCleared >= 1:
		return True
		
	return False

def TryDrop(DoWhat):
	global CurrentPiece
	# duplicate Game
	for x in range(col):
		for y in range(row):
			TryTetrisGame[y][x]=0	
	
	for x in range(col):
		for y in range(row):
			if TetrisGame[y][x] == 1:	
				TryTetrisGame[y][x] = 1
	
	if DoWhat == "Check":
		Collision=False
		while (Collision == False):			
			CurrentPiece=np.roll(CurrentPiece,1, axis=0)
			Collision=TryCheckCollision()
		return TryCheckForLineClear()

	if DoWhat == "GetPatterns":
		Collision=False
		while (Collision == False):
			CurrentPiece=np.roll(CurrentPiece,1, axis=0)
			Collision=TryCheckCollision()
		return GetAllPatterns(TryTetrisGame)
	
	raise ValueError('Error in Tetris.py -> "TryDrop(DoWhat)" function, The String given as argument was not recognised as any available string argument (available strings are "GetPatterns", "Check"')
	
if __name__ == '__init__':
    init()
	
def Documentation():
	#Debug()
	#os.system('CLS')
	#RightMove()
	#LeftMove()
	#Drop()
	#Rotate(piece,rotation)
	return null
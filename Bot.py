# coding=utf-8

import Tetris as Tetris
import random as rand
import numpy as np
import os
import time
import sys
from directkeys import ReleaseKey, PressKey, W, A, S, D, LEFT, RIGHT, UP, DOWN, C, SPACE
import pyHook,pythoncom
import win32api, win32con, win32gui
import Categories

GamesForBotToPlay=10
SwitchToHumanModeAt=9

HighestYs = [19 for i in range(0,10)] #depricated

Roughness =[0 for i in range(0,4*12)] 
Fuzziness = [0 for i in range(0,12*4)] 

CurrentRoughness =[0 for i in range(0,4*12)]
CurrentFuzziness  =[0 for i in range(0,12*4)]

DelayTime=0

def main():
	print("Move Time 3 sec")
	time.sleep(3)	
	global GamesForBotToPlay
	global SwitchToHumanModeAt
	GamesForBotToPlay=int(sys.argv[1])
	SwitchToHumanModeAt=int(sys.argv[2])
	Tetris.init()
	Tetris.TheBrick=Categories.GetBrick()
	Tetris.GiveNewPiece()
	print(Tetris.TheBrick)
	print("Press C Time 2 sec")
	time.sleep(2)
	Mode('robot')

def Mode(mode):
	global GamesForBotToPlay
	global SwitchToHumanModeAt
	global DelayTime
	if mode=='robot':
		while Tetris.timeslost !=GamesForBotToPlay:
			if Tetris.timeslost == SwitchToHumanModeAt: 	#switch to human mode at
				mode='human' 			#switch to human mode at
				break			 		#switch to human mode at
			MakeMove(Tetris.piece,Pattern())
			os.system('cls')			
			print('Games played:',Tetris.timeslost)
			print('Lines Cleared:',Tetris.pointOverGames)			
		os.system('cls')
		print("Games Played:",Tetris.timeslost)
		print("bot got",Tetris.pointOverGames, "lines cleared")
		if Tetris.pointOverGames == 0:
			print('The bot learned absolutely nothing!')
		print("Loading all done moves..")

	if mode=='human':
		while Tetris.timeslost !=GamesForBotToPlay:
			os.system('cls')
			Tetris.Debug()
			MakeMove(Tetris.piece,Pattern())			
			os.system('cls')
			print('Games played:',Tetris.timeslost)
			print('Lines Cleared:',Tetris.pointOverGames)
		os.system('cls')
	
def CheckForReward():
	if Tetris.botReward < Tetris.point:	
		Tetris.botReward = Tetris.point	

def Pattern(): 
	global HighestYs
	HighestYs = [19 for i in range(0,10)]
	for x in range(9, -1, -1):
		for y in range(19, -1, -1):
			if(Tetris.TetrisGame[y][x] == 1):
				HighestYs[x]=y
	return 0
		
def MakeMove(piece,pattern1Value):
	CheckIfCanClearLine()
	
	GetPatternsForAllMoves()
	LowestRoughNFuzz=0
	LowestRoughNFuzz=LowestRoughAndFuzz()

	Outputs(LowestRoughNFuzz) #0-47	
	

#0-47 
def Outputs(Output):
	SideMoves=12
	Orientations=4
	ResultMove=Output%SideMoves
	ResultOrientation=int(np.floor(Output/SideMoves))
	
	OutPutOrientation(ResultOrientation,False)
	if ResultMove > 5:
		OutPutRightMove(ResultMove-5,False)
	else:
		OutPutLeftMove(ResultMove,False)
	Tetris.Drop()
	CheckForReward()
	

def GetPatternsForAllMoves():
	for i in range(12*4):
		Output=i
		SideMoves=12
		Orientations=4
		ResultMove=Output%SideMoves
		ResultOrientation=int(np.floor(Output/SideMoves))
		
		OutPutOrientation(ResultOrientation,True)
		if ResultMove > 5:
			OutPutRightMove(ResultMove-5,True)
		else:
			OutPutLeftMove(ResultMove,True)
		
		Fuzziness[i],Roughness[i]=Tetris.TryDrop("GetPatterns")
	
	return 0
	
def CheckIfCanClearLine():
	for i in range(12*4):
		Output=i
		SideMoves=12
		Orientations=4
		ResultMove=Output%SideMoves
		ResultOrientation=int(np.floor(Output/SideMoves))
		
		OutPutOrientation(ResultOrientation,True)
		if ResultMove > 5:
			OutPutRightMove(ResultMove-5,True)
		else:
			OutPutLeftMove(ResultMove,True)
			
		if Tetris.TryDrop("Check"):
			Outputs(i)
			return 0

def LowestRoughAndFuzz():
	global Roughness
	global Fuzziness
	lowestRoughness=200;

	CompareRF=200
	CompareArrayRF=[0 for i in(0,48)]
	CompareLowestRough=200
	CompareLowestArrayRF=[0 for i in(0,48)]
	AlternativeMove=0

#-----------------	
	for i in range(len(Roughness)):
		if lowestRoughness > Roughness[i]:
			lowestRoughness=Roughness[i]

	for i in range(len(Roughness)):
		if Roughness[i] == lowestRoughness:
			if CompareRF > Roughness[i]+Fuzziness[i]:
				CompareRF=Roughness[i]+Fuzziness[i]
		
	for i in range(len(Roughness)):
		if CompareRF == Roughness[i]+Fuzziness[i]:
			AlternativeMove = i
			if lowestRoughness == Roughness[i]:
				return i

	
def OutPutLeftMove(Moves, IsTry):
	Tetris.LeftMove(Moves,Tetris.piece)
	if IsTry == False:
		time.sleep(0.1)
		for i in range(Moves):
			PressKey(LEFT)
			time.sleep(0.1)
			ReleaseKey(LEFT)
			time.sleep(0.1)
		PressKey(SPACE)
		time.sleep(0.1)
		ReleaseKey(SPACE)

			
def OutPutRightMove(Moves, IsTry):
	Tetris.RightMove(Moves,Tetris.piece)
	if IsTry == False:
		time.sleep(0.1)
		for i in range(Moves):
			PressKey(RIGHT)
			time.sleep(0.1)
			ReleaseKey(RIGHT)
			time.sleep(0.1)
		PressKey(SPACE)
		time.sleep(0.1)
		ReleaseKey(SPACE)

		
		
def OutPutOrientation(Orientation,IsTry):
	Tetris.rotation = Orientation
	Tetris.Rotate()
	if IsTry == False:	
		time.sleep(0.1)
		Tetris.TheBrick=Categories.GetBrick()
		for i in range(Orientation):
			PressKey(UP)
			time.sleep(0.1)
			ReleaseKey(UP)
			time.sleep(0.1)
	

if __name__ == '__main__':
    main()

def Documentation():

	return null

import Tetris as Tetris
import random as rand
import numpy as np
import json
import os
import time
import sys

row=20
col=10


def main():
	print("Test 1 GetRoughnessTestfor1Space Suceeded "+str(GetRoughnessTestfor1Space())+"")
	print("Test 2 GetRoughnessTestforMoreSpaces Suceeded "+str(GetRoughnessTestforMoreSpaces())+"")
	print("Test 3 GetRoughnessTestfor0Spaces Suceeded "+str(GetRoughnessTestfor0Spaces())+"")
	print("Test 4 GetFuzziness Suceeded "+str( GetFusinessTest1())+"")
	
	#GetFusinessTest1()
	
def resetArray(GameArray):
	for x in range(col):
		for y in range(row):
			GameArray[y][x]=0
			GameArray[y][x]=0
	return GameArray
	
def GetRoughnessTestfor1Space():
	Tetris.init()
	UnitTestTetrisGame = np.arange(row*col)
	UnitTestTetrisGame = UnitTestTetrisGame.reshape(row, col)
	UnitTestTetrisGame = resetArray(UnitTestTetrisGame)
	
	UnitTestTetrisGame[19][0]=0
	UnitTestTetrisGame[18][0]=1

	Tetris.GetHighestYs(UnitTestTetrisGame)

	Tetris.GetRoughness(UnitTestTetrisGame)
		
	if Tetris.roughness == 1:
		return True
	return False
		
	
def GetRoughnessTestforMoreSpaces():
	Tetris.init()
	UnitTestTetrisGame = np.arange(row*col)
	UnitTestTetrisGame = UnitTestTetrisGame.reshape(row, col)
	UnitTestTetrisGame = resetArray(UnitTestTetrisGame)
	
	UnitTestTetrisGame[19][0]=1
	UnitTestTetrisGame[18][0]=0
	UnitTestTetrisGame[17][0]=1
	
	UnitTestTetrisGame[19][6]=0
	UnitTestTetrisGame[18][6]=0
	UnitTestTetrisGame[17][6]=1
	
	UnitTestTetrisGame[19][3]=0
	UnitTestTetrisGame[18][3]=1
	
	Tetris.GetHighestYs(UnitTestTetrisGame)
	Tetris.GetRoughness(UnitTestTetrisGame)
		
	if Tetris.roughness == 4:
		return True
	return False

def GetRoughnessTestfor0Spaces():
	Tetris.init()
	UnitTestTetrisGame = np.arange(row*col)
	UnitTestTetrisGame = UnitTestTetrisGame.reshape(row, col)
	UnitTestTetrisGame = resetArray(UnitTestTetrisGame)
	Tetris.GetHighestYs(UnitTestTetrisGame)
	Tetris.GetRoughness(UnitTestTetrisGame)	
	if Tetris.roughness == 0:
		return True
	return False
	
def GetFusinessTest1():
	Tetris.init()
	UnitTestTetrisGame = np.arange(row*col)
	UnitTestTetrisGame = UnitTestTetrisGame.reshape(row, col)
	UnitTestTetrisGame = resetArray(UnitTestTetrisGame)
	
	UnitTestTetrisGame[19][0]=1
	UnitTestTetrisGame[18][0]=1
	UnitTestTetrisGame[17][0]=1
	UnitTestTetrisGame[19][1]=1
	
	
	UnitTestTetrisGame[19][3]=1
	UnitTestTetrisGame[18][3]=1

	UnitTestTetrisGame[19][7]=1
	
	UnitTestTetrisGame[19][9]=1
	
	
	Tetris.GetHighestYs(UnitTestTetrisGame)
	
	
	Tetris.GetFuzziness(UnitTestTetrisGame)
	
	if Tetris.fuzziness[0] == 2 and Tetris.fuzziness[3] == 2 and Tetris.fuzziness[7] == 1 and Tetris.fuzziness[8] == 1:
		return True
	return False

	
if __name__ == '__main__':
    main()

def Documentation():
	#tests fuctions
	return null

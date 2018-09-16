import math
import numpy as np
import time
import pyscreenshot as ImageGrab
import cv2

def categorise(contours):
	categoryResult=[]
	pieces=[]
	minx=0
	miny=0
	maxx=0
	maxy=0
	minxminy=0
	minxmaxy=0
	maxxmaxy=0
	maxxminy=0
	d1=0	
	d2=0
	slope1=0
	slope2=0
	for x in range(len(contours)):
		if x%2==1:
			for y in range(len(contours[x])):
				if contours[x][y][0][0] <= minx or minx == 0:
					if contours[x][y][0][0] != minx:
						minxmaxy=0
						minxminy=0
					minx=contours[x][y][0][0]
					if contours[x][y][0][1] > minxmaxy:
						minxmaxy=contours[x][y][0][1]
					if contours[x][y][0][1] < minxminy or minxminy == 0:
						minxminy=contours[x][y][0][1]						
				if contours[x][y][0][0] >= maxx:
					if contours[x][y][0][0] != maxx:
						maxxmaxy=0
						maxxminy=0
					maxx=contours[x][y][0][0]
					if contours[x][y][0][1] < maxxminy or maxxminy == 0:
						maxxminy=contours[x][y][0][1]
					if contours[x][y][0][1] > maxxmaxy:
						maxxmaxy=contours[x][y][0][1]
			d1 = round(math.hypot(maxx-minx, maxxmaxy-minxminy))
			d2 = round(math.hypot(maxx-minx, maxxminy-minxmaxy))
			minxminy=0
			minxmaxy=0
			maxxmaxy=0
			maxxminy=0
			maxx=0
			minx=0
			if d1 == 42 and d2==37:
				pieces.append('blå')
			if d1 == 42 and d2==35:
				pieces.append('rød')
			if d1 == 48 and d2==48:
				pieces.append('lyseblå')
			if d1 == 37 and d2==42:
				pieces.append('orange')
			if d1 == 37 and d2==37:
				pieces.append('lilla')
			if d1 == 35 and d2==42:
				pieces.append('grøn')
			if d1 == 33 and d2==33:
				pieces.append('gul')

			if d1 == 23 and d2==27:
				pieces.append('grøn')
			if d1 == 27 and d2==23:
				pieces.append('rød')
			if d1 == 27 and d2==24:
				pieces.append('blå')
			if d1 == 32 and d2==32:
				pieces.append('lyseblå')
			if d1 == 21 and d2==21:
				pieces.append('gul')
			if d1 == 24 and d2==27:
				pieces.append('orange')
			if d1 == 24 and d2==24:
				pieces.append('lilla')
	return pieces

def process_img(original_image):
	processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
	processed_img = cv2.Canny(processed_img, threshold1=1000, threshold2=600)
	return processed_img
	
def GetBrick():
	screen = np.array(ImageGrab.grab(bbox=(410, 330, 420+50, 360+265-30)))
	new_screen= process_img(screen)
	ret, threshold = cv2.threshold(new_screen, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	_, contours, _ = cv2.findContours(threshold, cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

	categoryResult=categorise(contours)

	try:
		return categoryResult[4]
	except:
		GetBrick()

	return 0

if __name__ == '__GetBrick__':
    GetBrick()
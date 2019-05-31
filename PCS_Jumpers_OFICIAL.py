import numpy as np
import cv2
import keyboard as kb
import imutils
from imutils.video import VideoStream
from time import sleep

x = 0
cont_zeros = 0
p1 = 20
p2 =  20
#cap = cv2.VideoCapture(0)
cap = VideoStream(src=0)
Oy = 0
flag_pulo = 4

def nothing(x):
	pass

cx = 0
cy = 0
last_cy = 0
flag = 0
flag2 = 0 
flag_ini = 0

cv2.namedWindow('frame')

cv2.createTrackbar('Hl', 'frame', 0,255,nothing)
cv2.createTrackbar('Hu', 'frame', 82,255,nothing)
cv2.createTrackbar('Sl', 'frame', 134,255,nothing)
cv2.createTrackbar('Su', 'frame', 255,255,nothing)
cv2.createTrackbar('Vl', 'frame', 110,255,nothing)
cv2.createTrackbar('Vu', 'frame', 255,255,nothing)

cap.start()

while(True):
	#ret, frame = cap.read()
	frame = cap.read()
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	hl = cv2.getTrackbarPos('Hl', 'frame')
	sl = cv2.getTrackbarPos('Sl', 'frame')
	vl = cv2.getTrackbarPos('Vl', 'frame')

	hu = cv2.getTrackbarPos('Hu', 'frame')
	su = cv2.getTrackbarPos('Su', 'frame')
	vu = cv2.getTrackbarPos('Vu', 'frame')

	lower_color = np.array([hl, sl, vl])
	upper_color = np.array([hu, su, vu])

	mask = cv2.inRange(hsv, lower_color, upper_color)
	kernel = np.ones((5,5), np.uint8)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

	segimg=cv2.bitwise_and(frame, frame, mask= mask)

	contours,____ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	
	center = []
	sum_1y = 0.0
	sum_2y = 0.0
	sum_1x = 0.0
	sum_2x = 0.0
	for c in contours:
		M = cv2.moments(c)
		sum_1y = sum_1y + M['m01']
		sum_2y = sum_2y + M['m00']
		sum_1x = sum_1x + M['m10']
		sum_2x = sum_2x + M['m00']
	try:
		cy = int(sum_1y/sum_2y)
		cx = int(sum_1x/sum_2x)
	except ZeroDivisionError:
		pass
		
	bat = np.array([cx, cy])
	if type(bat) is not np.int32:
		cv2.circle(segimg, tuple(bat), 2, (0,255,0), 10)
	
	if flag == 0:
		sleep(2)
		flag = 1   
		Oy = cy               
		last_cy = cy

	if cy > (last_cy+p1)  and Oy+34 < cy and flag_pulo >= 4:
		kb.press('s')
		sleep(0.500)
		kb.release('s')
		flag_pulo = 1
	elif cy < (last_cy-p2) and cy < Oy-15:
		kb.press_and_release('w')

	elif flag_pulo < 4:
		flag_pulo = flag_pulo+ 1

	

		
	last_cy = cy					

	cv2.imshow('frame', segimg)
	#cv2.imshow('mask', mask)
	#cv2.imshow('hsv', hsv)
	

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
cap.release()
cv2.destroyAllWindows()                                               


	


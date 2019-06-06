'''
 * @file jumpers_CV 
 *
 * @brief Real-time computer vision algorithm to track the Y-coordinate of a processed, segmented live video capture. 
 *
 * @author Felipe Bagni <febagni@usp.br>
 * @author Gabriel Kishida <gabriel.kishida@usp.br> 
 * @author Kevin Onishi	<kevintaiyo@usp.br>
 * 
 * @date 05/2019
 '''

'''**************************
 *@brief Importing Libraries
**************************'''
import numpy as np	#NumPy
import cv2	#OpenCV(4.1.0)

'''***************************************
 *@brief Initialization of some variables
***************************************'''
x = 0 #auxiliary variable
cont_zeros = 0	#counter used to avoid position variation error
p1 = 10	#roof value 
p2 =  10 #floor value
last_cy = 0 #retains the last value of the y coordiante from the point of interest to the following iteration
flag = 0 #flag to check the first occurrence of cy and last_cy comparison

'''@brief Initialization of the video capture'''
cap = cv2.VideoCapture(0) #captures the video of the USB WebCam

'''@brief Checks if the video was captured '''
def nothing(x):
	pass

'''@brief Creates a window called frame, where the analysis will take place'''
cv2.namedWindow('frame')

'''****************************************************************************************
 *@brief Creation of trackbars to adjust the HSV range with which the mask will be applied
****************************************************************************************'''
cv2.createTrackbar('Hl', 'frame', 0,255,nothing)
cv2.createTrackbar('Hu', 'frame', 65,255,nothing)
cv2.createTrackbar('Sl', 'frame', 65,255,nothing)
cv2.createTrackbar('Su', 'frame', 255,255,nothing)
cv2.createTrackbar('Vl', 'frame', 105,255,nothing)
cv2.createTrackbar('Vu', 'frame', 255,255,nothing)


while(True):
	ret, frame = cap.read()

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
		flag = 1
		last_cy = cy
		
	if cy > (last_cy+p1) :
		if cont_zeros > 10:
			print('-1')
			cont_zeros = 0
	elif cy < (last_cy-p2):
		if cont_zeros > 10:
			print('1')
			cont_zeros = 0
	else:
		print('0')
		cont_zeros = cont_zeros + 1
	
	if cont_zeros > 100:
		cont_zeros = 11	
		
	last_cy = cy					

	cv2.imshow('frame', segimg)
	#cv2.imshow('mask', mask)
	#cv2.imshow('hsv', hsv)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
cap.release()
cv2.destroyAllWindows()                                               


	


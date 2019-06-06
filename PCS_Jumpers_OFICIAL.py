'''
 * @file jumpers_CV 
 *
 * @brief Real-time computer vision algorithm to track the Y-coordinate of a processed, segmented live video capture. 
 *
 * @author Felipe Bagni <febagni@usp.br>
 * @author Gabriel Kishida <gabriel.kishida@usp.br> 
 * @author Kevin Onishi	<kevintaiyo@usp.br>
 * 
 * @date 06/2019
 '''

'''**************************
 *@brief Importing Libraries
**************************'''
import numpy as np #numpy to treat matrices and arrays (images)
import cv2 #OpenCV 4.1.O for computer vision
import keyboard as kb #keyboard emulation 
import imutils #video capture without buffer
from imutils.video import VideoStream
from time import sleep 

'''***************************************
 *@brief Initialization of some variables
***************************************'''
#auxiliary variable
x = 0
#parameter for jumping and crouching control
p1 = 20 
p2 =  20 
#origin of y coordinate set in the calibration
Oy = 0 
#last y coordinate read
last_cy = 0
#coordinates of the geometric center of the areas processed
cx = 0
cy = 0
#control flags
flag = 0
flag2 = 0 
flag_ini = 0
flag_pulo = 4

'''***************************************************
 *@brief Procedures to start the image processing
***************************************************'''
cap = VideoStream(src=0) #Initialization of the video streaming from webcam

def nothing(x): #Checks to proceed
	pass

cv2.namedWindow('frame') #Creates a window called frame, where the analysis will take place

#Creation of trackbars to adjust the HSV range with which the mask will be applied
cv2.createTrackbar('Hl', 'frame', 0,255,nothing)
cv2.createTrackbar('Hu', 'frame', 82,255,nothing)
cv2.createTrackbar('Sl', 'frame', 134,255,nothing)
cv2.createTrackbar('Su', 'frame', 255,255,nothing)
cv2.createTrackbar('Vl', 'frame', 110,255,nothing)
cv2.createTrackbar('Vu', 'frame', 255,255,nothing)

cap.start()	#Initialization of the video capture


'''**********************************************************************************************************
 *@brief Processing the images from the video stream and tracking the y position of the object being analyzed
***********************************************************************************************************'''
while(True):

	frame = cap.read()	#display in "frame" the video captured
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #tranforms the image from RGB to HSV

	# Save the alues from the trackbars
	hl = cv2.getTrackbarPos('Hl', 'frame')
	sl = cv2.getTrackbarPos('Sl', 'frame')
	vl = cv2.getTrackbarPos('Vl', 'frame')
	hu = cv2.getTrackbarPos('Hu', 'frame')
	su = cv2.getTrackbarPos('Su', 'frame')
	vu = cv2.getTrackbarPos('Vu', 'frame')

	#Create arrays with the upper and lowwer values of the range created for H, S and V.
	lower_color = np.array([hl, sl, vl])
	upper_color = np.array([hu, su, vu])

	mask = cv2.inRange(hsv, lower_color, upper_color) #Creating and applying a mask to showcase only the colors set with the trackbars

	#Making the "opening" of the image by eroding and then dilating the areas after the mask was applied, getting reduce the noise
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

	#Segmenting the image after the opening 
	segimg=cv2.bitwise_and(frame, frame, mask= mask)

	#Finding the contours of the resulting areas
	contours,____ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	
	#Creating sum variables to find the y and x position of the geometric centre of the areas 
	sum_1y = 0.0
	sum_2y = 0.0
	sum_1x = 0.0
	sum_2x = 0.0

	#Finding the x and y coordinate of the geometric centre by the weighted average of the areas
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
	
	#Drawing a green circle in the centre
	if type(bat) is not np.int32:
		cv2.circle(segimg, tuple(bat), 2, (0,255,0), 10)
	
	#Calibrating some variables for the y-axis tracking
	if flag == 0:
		sleep(2)
		flag = 1   
		Oy = cy               
		last_cy = cy

	#Analysing if the object has moved downwards (if the person crouched)
	if cy > (last_cy+p1)  and Oy+34 < cy and flag_pulo >= 4:
		kb.press('s') #emulating the "crouch" key on the keyboard (enabling the game to be played)
		sleep(0.500)
		kb.release('s')
		flag_pulo = 1

	#Analysing if the object has moved upwards (if the person jumped)
	elif cy < (last_cy-p2) and cy < Oy-15:
		kb.press_and_release('w') #emulating the "jump" key on the keyboard (enabling the game to be played)

	#Flag to help in the control of the jump_falling and crouching difference
	elif flag_pulo < 4:
		flag_pulo = flag_pulo+ 1

	#Updating the last value of Y
	last_cy = cy			

	#Displaying "frame" with the segmentation applied	
	cv2.imshow('frame', segimg)
	
	#Ending the code with ctrl+C or 'q' keys	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

#Ending the video capture and closing all windows opened during execution	
cap.release()
cv2.destroyAllWindows()                                               


	


import numpy as np     #biblioteca numpy para trabalhar com matriz (img)
import cv2 #importa o opencv
from time import sleep

x=0
cap = cv2.VideoCapture(0) #acessa a camera na entrada padrao do rasp = 0

def nothing(x):
    pass 

readings=[]
average=0
last_vlue=0

cv2.namedWindow('frame')

cv2.createTrackbar('Hl','frame',46,255,nothing)
cv2.createTrackbar('Hu','frame',87,255,nothing)
cv2.createTrackbar('Sl','frame',40,255,nothing)
cv2.createTrackbar('Su','frame',140,255,nothing)
cv2.createTrackbar('Vl','frame',0,255,nothing)
cv2.createTrackbar('Vu','frame',255,255,nothing)


while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    hl = cv2.getTrackbarPos('Hl', 'frame')
    sl = cv2.getTrackbarPos('Sl', 'frame')
    vl = cv2.getTrackbarPos('Vl', 'frame')
    hu = cv2.getTrackbarPos('Hu', 'frame')
    su = cv2.getTrackbarPos('Su', 'frame')
    vu = cv2.getTrackbarPos('Vu', 'frame')
    
    #lower_color = np.array([46, 40, 0])
    #upper_color = np.array([87, 140, 255])
    lower_color = np.array([hl, sl, vl])
    upper_color = np.array([hu, su, vu])
    
    mask = cv2.inRange(hsv, lower_color, upper_color)
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel)
    
    segimg=cv2.bitwise_and(frame, frame, mask= mask)
    
    cv2.imshow('frame',segimg)
    cv2.imshow('mask',mask)
    cv2.imshow('hsv',hsv)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
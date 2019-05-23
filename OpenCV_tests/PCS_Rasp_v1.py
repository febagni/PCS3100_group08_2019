import numpy as np     #biblioteca numpy para trabalhar com matriz (img)
import RPi.GPIO as GPIO #usar as saidas do rasp para controlar o servo/ habilita a gpio ndo rasp para deixA la como se fosse um arduino
import cv2 #importa o opencv
from time import sleep

x=0
cap = cv2.VideoCapture(0) #acessa a camera na entrada padrao do rasp = 0

def nothing(x):
    pass 

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)
pwm=GPIO.PWM(11,50)
pwm.start(5)



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
    if ret==False:
        x+=1
        if x>10:
            break
        continue
    
        

    # Our operations on the frame come here
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

    __, contours,__ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    center = []

    for c in contours:    
        M = cv2.moments(c)
        try:
            center.append([ int(M['m10']/M['m00']), int(M['m01']/M['m00']) ])

        except ZeroDivisionError:
            pass

        # print(M['m10'], M['m00'], c)

    bat = np.array(center)
    bat = np.mean(bat, axis = 0, dtype=int)    
    #print(type(bat))
    #print(bat)
    if type(bat) is np.int32:
        print("Senhor do Universo")
    else:
        cv2.circle(segimg, tuple(bat), 2, (0,255,0), 10)
        
        bat = float(bat[0])/mask.shape[1]         #map para a resolucao da imagem e posicao no eixo x -> de 0 a 1
        #print(mask.shape)
        readings.append(bat)
        if(len(readings)>=10):
             readings.pop(0)
        average=float(sum(readings))/len(readings)
        MAX = 11
        MIN = 5
        average = average*(MIN-MAX)+MAX
        
        print(average)
        
        #if int(average)==last_vlue:
        #    pwm.stop()
        #else:
        #   pwm.start(last_vlue)
        pwm.ChangeDutyCycle(int(average))
        #pwm.stop()
        #last_vlue=int(average)

     # Display the resulting frame
    
    cv2.imshow('frame',segimg)
    '''cv2.imshow('mask',mask)
    cv2.imshow('hsv',hsv)'''
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

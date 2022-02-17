import cv2
import time
import numpy as np

fourcc = cv2.VideoWriter_fourcc(*'XVID')
# To save save an output in a file output.avi
output_file = cv2.VideoWriter('output.avi',fourcc,20.0,(640,480))
cam = cv2.VideoCapture(1)
time.sleep(2)
bg = 0
for i in range (60) :
    ret,bg  = cam.read()
bg = np.flip(bg,axis = 1)
while (cam.isOpened()) :
    ret,img = cam.read()
    if not ret :
        break
    img = np.flip(img,axis = 1)
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)  
    lowerRED = np.array([0,120,50]) 
    upperRED = np.array([10,255,255]) 
    mask1 = cv2.inRange(hsv,lowerRED,upperRED)
    lowerRED = np.array([170,120,70]) 
    upperRED = np.array([180,255,255]) 
    mask2 = cv2.inRange(hsv,lowerRED,upperRED)
    mask1 = mask1+mask2
    mask1 = cv2.morphologyEx(mask1,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
    mask1 = cv2.morphologyEx(mask1,cv2.MORPH_DILATE,np.ones((3,3),np.uint8))
    output = cv2.bitwise_not(mask1)
    result1 = cv2.bitwise_and(img,img,mask = output)
    result2 = cv2.bitwise_and(bg,bg,mask = mask1)
    final_output = cv2.addWeighted(result1,1,result2,1,0)
    output_file.write(final_output)
    cv2.imshow('Magic',final_output)
    cv2.waitKey(1)
cam.release()
output.release()
cv2.destroyAllWindows()
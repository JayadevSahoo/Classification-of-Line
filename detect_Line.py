# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 18:40:49 2019

@author: jaya
"""

import cv2
import os
#import numpy as np
it=1

def paragraphSegment(file_name):
    global it
    img = cv2.imread(file_name)
    
    img2gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_s1 =GetSmoothing(img2gray)   #replace img2gray to img_s1
    #this thresold is for bitwise_and operator
    ret,mask=cv2.threshold(img_s1,180,255,cv2.THRESH_BINARY)
    image_final=cv2.bitwise_and(img_s1, img_s1 ,mask=mask)
    #cv2.imshow("Bitwise",image_final)
    ret,new_img =cv2.threshold(image_final,180,255,cv2.THRESH_BINARY)
    color_negative=abs(255-new_img)
    #cv2.imshow("Blackwhite",Color_negative)
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(8,8))
    dilated = cv2.dilate(color_negative, kernel,iterations =7)
    out_dir=r"G:/Project/PageClassification"
    os.chdir(out_dir)
    
    cv2.imwrite('dilute.jpg',dilated)
    
    
    contours,hierarchy = cv2.findContours(dilated,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    
    countPara = 0
    for contour in contours:
         [x,y,w,h] =cv2.boundingRect(contour)
         if w < 150 and h < 20:
             continue
         countPara =countPara+1
         cv2.rectangle (img, (x,y), (x+w ,y+h),(0,240,0),4)
         
         #cropped =img_final[y: y+h, x: x+w]
         #s = file_name+ '/crop' +str(index)+ '.jpg'
        # cv2.imwrite(s ,cropped)
         #index =index+1
        
    return img,countPara

def GetSmoothing(image):
    img_s = cv2.GaussianBlur(image,(6,6),0) #paragraph identification
    return img_s

if __name__=="__main__":
    img_dir = r"G:/Project/Page"
    out_dir=r"G:/Project/PageClassification"
    os.chdir(img_dir)
    i=1
    for pdf_file in os.listdir(img_dir):
        #print (pdf_file)
        #print(i)
        para_img, para_cnt=paragraphSegment(pdf_file)
        print('Number of paragraph in Page'+str(i) , para_cnt)
        os.chdir(out_dir)
        cv2.imwrite('page'+str(i)+'.jpg',para_img)
        i=i+1
        os.chdir(img_dir)












         
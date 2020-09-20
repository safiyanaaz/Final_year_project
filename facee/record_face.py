# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 17:34:55 2020

@author: Lenovo
"""

import cv2
import numpy as np 
import sqlite3
import os
import pyttsx3
engine =pyttsx3.init()
rate = engine.getProperty('rate')   # getting details of current speaking rate
engine.setProperty('rate', 125)     # setting up new voice rate
"""VOLUME"""
volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1                      
#printing current volume level
engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1
"""VOICE"""
voices = engine.getProperty('voices')    

conn = sqlite3.connect('face.db')
if not os.path.exists('./dataset'):
    os.makedirs('./dataset')
c = conn.cursor()
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
engine.say("Enter Name of The Person")
engine.runAndWait()
engine.stop()
uname = input("Enter your name: ")
c.execute('INSERT INTO users (name) VALUES (?)', (uname,))
uid = c.lastrowid
sampleNum = 0
while True:
  ret, img = cap.read()
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  cv2.imshow('pic', gray)
  faces = face_cascade.detectMultiScale(gray, 1.3, 5)
  for (x,y,w,h) in faces:
    sampleNum = sampleNum+1
    cv2.imwrite("dataset/User."+str(uid)+"."+str(sampleNum)+".jpg",gray[y:y+h,x:x+w])
    cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
    cv2.waitKey(100)
  cv2.waitKey(1);
  if sampleNum > 100:
    break
cap.release()
conn.commit()
conn.close()
cv2.destroyAllWindows()

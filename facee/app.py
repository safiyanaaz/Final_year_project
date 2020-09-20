from flask import Flask,render_template,url_for,request
import pandas as pd
import numpy as np
import base64
from PIL import Image
from io import BytesIO
import cv2
import re
import pyttsx3
from flask import jsonify
import os
import time
import sqlite3
import os,io
import pandas as pd
import create_database


app = Flask(__name__)


@app.route('/')
def index():

	return render_template('layout.html')


@app.route('/predict',methods=['GET', 'POST'])

def predict():

	if request.method=='POST':
		input=reqquest.form.get("text") if request.form.get("input") else None
		print(input)
		input1= request.form.get("input1") if request.form.get("input1") else None
		base64_data = re.sub('^data:image/.+;base64,', '',input1)
		print(input1)
		im = Image.open(input)
		im = im.convert('RGB')
		im.save('image.jpg')
		im.save('image.jpg', 'JPEG')
		print('image saved')
        # imag = Image.open('image.jpg')
		# data = asarray(imag)
        # print(type(imag))
        # print(data.shape)

	conn = sqlite3.connect('face.db')
	c = conn.cursor()
	fname = "recognizer/trainedData.yml"
	if not os.path.isfile(fname):
	  print("Please train the data first")
	  exit(0)
	face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
	# cap = cv2.VideoCapture(0)
	recognizer = cv2.face.LBPHFaceRecognizer_create()
	recognizer.read(fname)
	while True:
	  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	  faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	  for (x,y,w,h) in faces:
	    cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
	    ids,conf = recognizer.predict(gray[y:y+h,x:x+w])
	    c.execute("select name from users where id = (?);", (ids,))
	    result = c.fetchall()
	    name = result[0][0]
	    if conf < 50:
	      cv2.putText(img, name, (x+2,y+h-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (150,255,0),2)
	      flag=0
	    else:
	      cv2.putText(img, 'No Match', (x+2,y+h-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),2)
	      flag=1
	  cv2.imshow('Face Recognizer',img)
	  k = cv2.waitKey(30) & 0xff
	  if k == 27:
	    break
	cap.release()
	cv2.destroyAllWindows()

	if flag ==0:
	    engine.say(name)
	    engine.say('is in front of you')
	    engine.runAndWait()
	    engine.stop()
	else:
	    engine.say('No Match')
	    engine.runAndWait()
	    engine.stop()
	if flag == 1:
	    os.system("python record_face.py 1")
	    os.system("python trainer.py 1")

	return render_template('result.html',text="Face Recognition")


if __name__ == '__main__':
    app.run(debug=True)
